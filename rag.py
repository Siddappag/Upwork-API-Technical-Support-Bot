"""
RAG (Retrieval-Augmented Generation) Module
Handles document retrieval and LLM integration with DeepInfra
"""

import os
# Disable all telemetry BEFORE any other imports
os.environ['CHROMADB_TELEMETRY_DISABLED'] = 'true'
os.environ['OTEL_SDK_DISABLED'] = 'true'
os.environ['OTEL_EXPORTER_OTLP_INSECURE'] = 'true'

import shutil
import time
from typing import Tuple
from dotenv import load_dotenv
import requests
import json
import warnings

# Suppress chromadb and opentelemetry warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*chromadb.*")
warnings.filterwarnings("ignore", message=".*opentelemetry.*")

from utils.loader import load_pdf
from utils.retriever import Retriever, create_chunks
from utils.embeddings import EmbeddingGenerator
from utils.vectorstore import VectorStore

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class RAGBot:
    """RAG-based AI bot for Upwork API support."""
    
    def __init__(self, persist_dir: str = None):
        """
        Initialize RAG bot with vector store and LLM.
        
        Args:
            persist_dir: Path to persistent vector database
        """
        load_dotenv()
        
        # Use default path if not provided
        if persist_dir is None:
            persist_dir = os.path.join(SCRIPT_DIR, "chroma_db")
        
        # Initialize components
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = self._initialize_vector_store(persist_dir)
        self.retriever = Retriever(self.vector_store, self.embedding_generator)
        
        # Load system prompt
        prompt_path = os.path.join(SCRIPT_DIR, "prompts", "system_prompt.txt")
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read().strip()
        
        # Load DeepInfra config
        self.api_key = os.getenv("DEEPINFRA_API_KEY")
        self.model = os.getenv("DEEPINFRA_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")
        self.base_url = os.getenv("DEEPINFRA_BASE_URL", "https://api.deepinfra.com/v1/openai")
        
        if not self.api_key:
            raise ValueError("DEEPINFRA_API_KEY not set in environment variables")
        
        print("✓ RAG Bot initialized successfully")

    def _initialize_vector_store(self, persist_dir: str) -> VectorStore:
        """Initialize the vector store and rebuild it from the PDF when needed."""
        try:
            vector_store = VectorStore(persist_dir=persist_dir)
            if vector_store.get_collection_size() == 0:
                self._ingest_documents(vector_store)
            return vector_store
        except Exception as error:
            print(f"Vector store bootstrap failed: {error}")
            if os.path.exists(persist_dir):
                shutil.rmtree(persist_dir)

            vector_store = VectorStore(persist_dir=persist_dir)
            self._ingest_documents(vector_store)
            return vector_store

    def _ingest_documents(self, vector_store: VectorStore) -> None:
        """Build a fresh vector store from the bundled PDF."""
        pdf_path = os.path.join(SCRIPT_DIR, "data", "upwork_api_reference.pdf")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")

        text = load_pdf(pdf_path)
        chunks = create_chunks(text, chunk_size=500, chunk_overlap=50)
        embeddings = self.embedding_generator.generate_embeddings(chunks).tolist()
        vector_store.add_documents(chunks, embeddings)
    
    def retrieve_context(self, query: str) -> Tuple[list, list]:
        """
        Retrieve relevant chunks from vector database.
        
        Args:
            query: User question
            
        Returns:
            Tuple of (chunks, relevance_scores)
        """
        chunks, scores = self.retriever.retrieve(query)
        return chunks, scores
    
    def generate_answer(self, query: str, context_chunks: list) -> Tuple[str, float]:
        """
        Generate answer using DeepInfra LLM with retrieved context.
        
        Args:
            query: User question
            context_chunks: Retrieved context chunks
            
        Returns:
            Tuple of (answer, response_time_seconds)
        """
        start_time = time.time()
        
        # Check if context is empty
        if not context_chunks or all(chunk.strip() == "" for chunk in context_chunks):
            return "I'm sorry, but the provided documentation does not contain that information.", 0.0
        
        # Build context string
        context = "\n\n".join([f"[Source {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)])
        
        # Build user message
        user_message = f"""Based on the following Upwork API documentation context, answer this question:

Question: {query}

Context:
{context}

Answer:"""
        
        # Call DeepInfra API
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": self.system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            elapsed_time = time.time() - start_time
            return answer, elapsed_time
            
        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time
            error_msg = f"Error calling DeepInfra API: {str(e)}"
            print(error_msg)
            return error_msg, elapsed_time
    
    def answer_question(self, query: str) -> Tuple[str, list, float]:
        """
        Full RAG pipeline: retrieve and generate answer.
        
        Args:
            query: User question
            
        Returns:
            Tuple of (answer, source_chunks, total_time)
        """
        start_time = time.time()
        
        # Retrieve
        chunks, scores = self.retrieve_context(query)
        
        # Generate
        answer, gen_time = self.generate_answer(query, chunks)
        
        total_time = time.time() - start_time
        
        return answer, chunks, total_time
