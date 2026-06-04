"""
Document Ingestion Module
Loads PDF, chunks documents, generates embeddings, and stores in vector database
Run this once to prepare the knowledge base
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.loader import load_pdf, perform_sanity_check
from utils.embeddings import EmbeddingGenerator
from utils.vectorstore import VectorStore
from utils.retriever import create_chunks

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    """Main ingestion pipeline."""
    
    print("=" * 60)
    print("UPWORK API RAG BOT - DOCUMENT INGESTION")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Define paths
    pdf_path = os.path.join(SCRIPT_DIR, "data", "upwork_api_reference.pdf")
    persist_dir = os.path.join(SCRIPT_DIR, "chroma_db")
    
    # Step 1: Load PDF
    print("\n[Step 1] Loading PDF Document...")
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF not found at {pdf_path}")
        print(f"Please place your Upwork API PDF at: {pdf_path}")
        return
    
    text = load_pdf(pdf_path)
    print(f"✓ PDF loaded successfully")
    
    # Step 2: Sanity Check
    print("\n[Step 2] Performing Sanity Check...")
    char_count, first_500 = perform_sanity_check(text)
    print(f"Characters Loaded: {char_count:,}")
    print(f"\nSample (first 500 characters):")
    print("-" * 60)
    print(first_500)
    print("-" * 60)
    
    # Step 3: Chunk Documents
    print("\n[Step 3] Chunking Documents...")
    chunks = create_chunks(text, chunk_size=500, chunk_overlap=50)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Step 4: Generate Embeddings
    print("\n[Step 4] Generating Embeddings...")
    embedding_generator = EmbeddingGenerator()
    embeddings = embedding_generator.generate_embeddings(chunks)
    print(f"✓ Generated embeddings with shape: {embeddings.shape}")
    
    # Step 5: Store in Vector Database
    print("\n[Step 5] Storing in Vector Database...")
    vector_store = VectorStore(persist_dir=persist_dir)
    
    # Convert embeddings to list format for ChromaDB
    embeddings_list = embeddings.tolist()
    vector_store.add_documents(chunks, embeddings_list)
    
    collection_size = vector_store.get_collection_size()
    print(f"✓ Vector database created with {collection_size} documents")
    
    print("\n" + "=" * 60)
    print("INGESTION COMPLETE!")
    print("=" * 60)
    print(f"Database persisted at: {persist_dir}")
    print("You can now run: streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
