"""
Vector Store Module
Manages ChromaDB for storing and retrieving embeddings
"""

import chromadb
from typing import List, Tuple
import os


class VectorStore:
    """Manage ChromaDB vector database for document embeddings."""
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        """
        Initialize ChromaDB vector store with persistence.
        
        Args:
            persist_dir: Directory to persist the database
        """
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="upwork_api_docs",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"ChromaDB initialized with persistence at: {persist_dir}")
    
    def add_documents(self, chunks: List[str], embeddings: List[List[float]]) -> None:
        """
        Add document chunks and embeddings to vector store.
        
        Args:
            chunks: List of document chunks
            embeddings: List of embeddings for each chunk
        """
        # Generate IDs for each chunk
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": "upwork_api_docs", "chunk_index": i} for i in range(len(chunks))]
        )
        print(f"Added {len(chunks)} chunks to vector store")
    
    def search(self, query_embedding: List[float], top_k: int = 3) -> Tuple[List[str], List[float]]:
        """
        Search for most relevant chunks using embedding similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            
        Returns:
            Tuple of (retrieved_chunks, distances)
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if results['documents']:
            chunks = results['documents'][0]
            distances = results['distances'][0] if 'distances' in results else []
            return chunks, distances
        
        return [], []
    
    def get_collection_size(self) -> int:
        """Get number of documents in collection."""
        return self.collection.count()
