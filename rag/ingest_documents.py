"""
Script to ingest PDF documents from the data directory, extract text, split into chunks,
generate embeddings, and store in a ChromaDB collection.

This script should be run before using the RAG Q&A system to ensure the knowledge base
is up to date with the latest documents.
"""

import os
import pathlib
import sys
from typing import List, Dict, Any

import openai
from openai import OpenAI
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

# Try to import streamlit for secrets, but don't fail if not available
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

def get_chroma_client():
    """
    Initialize and return a ChromaDB client with in-memory storage.
    This avoids SQLite version compatibility issues.
    
    Returns:
        chromadb.Client: Initialized ChromaDB client
    """
    # Use the EphemeralClient which doesn't require SQLite
    client = chromadb.EphemeralClient()
    
    return client

def get_openai_api_key():
    """
    Get the OpenAI API key from environment variables, Streamlit secrets, or user input.
    
    Returns:
        str: OpenAI API key
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Try to get API key from environment variables
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")
    
    # If not found in environment variables, try Streamlit secrets
    if not api_key and STREAMLIT_AVAILABLE:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            pass
    
    # If still not found, prompt the user
    if not api_key:
        print("OpenAI API key not found in environment variables or Streamlit secrets.")
        api_key = input("Please enter your OpenAI API key: ")
        
        if not api_key:
            print("Error: No API key provided. Exiting.")
            sys.exit(1)
    
    return api_key

def main():
    """
    Main function to ingest documents from the data directory.
    """
    # Get OpenAI API key
    api_key = get_openai_api_key()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Get the data directory path
    data_dir = pathlib.Path(os.path.dirname(__file__)) / "data"
    
    # Check if data directory exists
    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        return
    
    # Get list of PDF files in the data directory
    filenames = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    
    if not filenames:
        print(f"No PDF files found in {data_dir}")
        return
    
    print(f"Found {len(filenames)} PDF files: {', '.join(filenames)}")
    
    # Initialize ChromaDB client and create/get collection
    try:
        chroma_client = get_chroma_client()
        
        # Create or get the collection for diabetes nutrition documents
        collection_name = "diabetes_nutrition_docs"
        
        # Check if collection exists and delete it to start fresh
        try:
            existing_collections = chroma_client.list_collections()
            if any(collection.name == collection_name for collection in existing_collections):
                print(f"Removing existing collection: {collection_name}")
                chroma_client.delete_collection(collection_name)
        except Exception as e:
            print(f"Error checking existing collections: {str(e)}")
        
        # Create a new collection
        collection = chroma_client.create_collection(
            name=collection_name,
            metadata={"description": "Diabetes and nutrition documents"}
        )
        
        print(f"Created ChromaDB collection: {collection_name}")
    except Exception as e:
        print(f"Error initializing ChromaDB: {str(e)}")
        return
    
    # Process each PDF file
    total_chunks_added = 0
    for filename in filenames:
        print(f"Processing {filename}...")
        
        # Extract text from the PDF file
        try:
            md_text = pymupdf4llm.to_markdown(data_dir / filename)
            print(f"  Extracted {len(md_text)} characters of text")
        except Exception as e:
            print(f"  Error extracting text from {filename}: {str(e)}")
            continue
        
        # Split the text into smaller chunks
        try:
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                model_name="gpt-4o", chunk_size=500, chunk_overlap=125
            )
            texts = text_splitter.create_documents([md_text])
            print(f"  Split into {len(texts)} chunks")
        except Exception as e:
            print(f"  Error splitting text from {filename}: {str(e)}")
            continue
        
        # Prepare data for ChromaDB
        chunk_ids = []
        chunk_texts = []
        chunk_embeddings = []
        chunk_metadatas = []
        
        # Generate embeddings for each chunk and prepare for ChromaDB
        for i, text in enumerate(texts):
            try:
                chunk_id = f"{filename}-{(i + 1)}"
                print(f"  Generating embedding for chunk {i+1}/{len(texts)}...", end="\r")
                
                # Generate embedding
                embedding = client.embeddings.create(
                    model="text-embedding-3-small", 
                    input=text.page_content
                ).data[0].embedding
                
                # Add to lists for batch addition
                chunk_ids.append(chunk_id)
                chunk_texts.append(text.page_content)
                chunk_embeddings.append(embedding)
                chunk_metadatas.append({
                    "source": filename,
                    "chunk_index": i + 1,
                    "total_chunks": len(texts)
                })
            except Exception as e:
                print(f"\n  Error generating embedding for chunk {i+1} of {filename}: {str(e)}")
                continue
        
        # Add chunks to ChromaDB collection in batches
        try:
            if chunk_ids:
                collection.add(
                    ids=chunk_ids,
                    documents=chunk_texts,
                    embeddings=chunk_embeddings,
                    metadatas=chunk_metadatas
                )
                print(f"  Added {len(chunk_ids)} chunks to ChromaDB collection")
                total_chunks_added += len(chunk_ids)
            else:
                print("  No chunks to add for this file")
        except Exception as e:
            print(f"  Error adding chunks to ChromaDB: {str(e)}")
    
    # Print success message
    print(f"Successfully added {total_chunks_added} chunks to ChromaDB collection '{collection_name}'")
    
    print("Document ingestion complete!")

if __name__ == "__main__":
    main()
