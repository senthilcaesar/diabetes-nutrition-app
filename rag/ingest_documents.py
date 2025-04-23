"""
Script to ingest PDF documents from the data directory, extract text, split into chunks,
generate embeddings, and save to a JSON file.

This script should be run before using the RAG Q&A system to ensure the knowledge base
is up to date with the latest documents.
"""

import json
import os
import pathlib
import sys
from typing import List, Dict, Any

import openai
from openai import OpenAI
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Try to import streamlit for secrets, but don't fail if not available
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

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
    
    # Process each PDF file
    all_chunks = []
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
            file_chunks = [{"id": f"{filename}-{(i + 1)}", "text": text.page_content} for i, text in enumerate(texts)]
            print(f"  Split into {len(file_chunks)} chunks")
        except Exception as e:
            print(f"  Error splitting text from {filename}: {str(e)}")
            continue
        
        # Generate embeddings for each chunk
        for i, file_chunk in enumerate(file_chunks):
            try:
                print(f"  Generating embedding for chunk {i+1}/{len(file_chunks)}...", end="\r")
                file_chunk["embedding"] = (
                    client.embeddings.create(model="text-embedding-3-small", input=file_chunk["text"]).data[0].embedding
                )
            except Exception as e:
                print(f"\n  Error generating embedding for chunk {i+1} of {filename}: {str(e)}")
                continue
        
        print(f"  Generated embeddings for {len(file_chunks)} chunks")
        all_chunks.extend(file_chunks)
    
    # Save the chunks with embeddings to a JSON file
    output_file = "rag_ingested_chunks.json"
    try:
        with open(output_file, "w") as f:
            json.dump(all_chunks, f, indent=4)
        print(f"Successfully saved {len(all_chunks)} chunks to {output_file}")
    except Exception as e:
        print(f"Error saving chunks to {output_file}: {str(e)}")
    
    print("Document ingestion complete!")

if __name__ == "__main__":
    main()
