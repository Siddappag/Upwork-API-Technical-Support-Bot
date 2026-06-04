"""
Retriever Module
Handles document retrieval based on user queries
"""

from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.embeddings import EmbeddingGenerator
from utils.vectorstore import VectorStore


class Retriever:
    """Retrieve relevant documents based on queries using RAG."""
    
    def __init__(self, vector_store: VectorStore, embedding_generator: EmbeddingGenerator):
        """
        Initialize retriever.
        
        Args:
            vector_store: VectorStore instance
            embedding_generator: EmbeddingGenerator instance
        """
        self.vector_store = vector_store
        self.embedding_generator = embedding_generator
        self.top_k = 3  # Number of chunks to retrieve
    
    def retrieve(self, query: str) -> Tuple[List[str], List[float]]:
        """
        Retrieve top-k most relevant chunks for a query.
        
        Args:
            query: User query text
            
        Returns:
            Tuple of (retrieved_chunks, relevance_scores)
        """
        # Generate embedding for query
        query_embedding = self.embedding_generator.embed_query(query).tolist()
        
        # Search vector store
        chunks, distances = self.vector_store.search(query_embedding, top_k=self.top_k)
        
        return chunks, distances


def create_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        text: Text to split
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_text(text)
    print(f"Created {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    
    return chunks
