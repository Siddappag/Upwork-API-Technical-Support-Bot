"""
Embedding Generation Module
Creates embeddings for document chunks using sentence-transformers
"""

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings using sentence-transformers locally."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding model.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully")
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            numpy array of embeddings (shape: [len(texts), embedding_dim])
        """
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print("Embeddings generated successfully")
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector
        """
        return self.model.encode([query])[0]
