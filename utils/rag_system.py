"""
RAG (Retrieval-Augmented Generation) system for the Diabetes Nutrition App.
This module provides functions for retrieving relevant information from PDF documents
and generating responses to user questions using Pinecone for vector storage and retrieval.
"""

import os
import pathlib
from typing import List, Dict, Any, Tuple, Optional, Union

import streamlit as st
from openai import OpenAI

from rag.pinecone_utils import similarity_search, ingest_documents as pinecone_ingest_documents

def get_openai_api_key():
    """
    Get the OpenAI API key from environment variables or Streamlit secrets.
    
    Returns:
        str: OpenAI API key
    """
    # Try to get API key from Streamlit secrets
    api_key = st.secrets.get("OPENAI_API_KEY")
    
    # If not found in Streamlit secrets, try environment variables
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables or Streamlit secrets.")
    
    return api_key

def ingest_documents(data_dir: str, index_name: str = "diabetes-nutrition") -> int:
    """
    Process PDF documents in the data directory, extract text, split into chunks,
    generate embeddings, and store in a Pinecone index.
    
    Args:
        data_dir: Path to directory containing PDF files
        index_name: Name of the Pinecone index to store documents
        
    Returns:
        int: Number of chunks added to the index
    """
    # Get list of PDF files in the data directory
    data_path = pathlib.Path(data_dir)
    file_paths = [str(data_path / f) for f in os.listdir(data_path) if f.endswith('.pdf')]
    
    # Ingest documents using Pinecone
    return pinecone_ingest_documents(file_paths, index_name)

def find_similar_chunks(question: str, index_name: str = "diabetes-nutrition", top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
    """
    Find chunks most similar to the question using Pinecone's similarity search.
    
    Args:
        question: User question
        index_name: Name of the Pinecone index
        top_k: Number of most similar chunks to return
        
    Returns:
        List of tuples containing chunks and their similarity scores
    """
    # Query Pinecone for similar chunks
    results = similarity_search(question, index_name, top_k)
    
    # Format results as list of tuples (chunk, similarity)
    similar_chunks = []
    for result in results:
        chunk = {
            "id": result["id"],
            "text": result["text"],
            "metadata": result["metadata"]
        }
        similarity = result["score"]
        
        similar_chunks.append((chunk, similarity))
    
    return similar_chunks

def generate_response(question: str, relevant_chunks: List[Tuple[Dict[str, Any], float]], model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Generate a response using the question and relevant chunks as context.
    
    Args:
        question: User question
        relevant_chunks: List of tuples containing relevant chunks and their similarity scores
        model: OpenAI model to use for response generation
        
    Returns:
        Dictionary containing the response and source information
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=get_openai_api_key())
    
    # Create context from relevant chunks
    context_parts = []
    sources = []
    
    for i, (chunk, score) in enumerate(relevant_chunks):
        # Only include chunks with similarity above a threshold
        if score < 0.7 and i >= 2:  # Include at least 2 chunks regardless of score
            continue
            
        context_parts.append(f"[{i+1}] {chunk['text']}")
        
        # Extract source from metadata if available, otherwise from ID
        if 'metadata' in chunk and 'source' in chunk['metadata']:
            source_id = chunk['metadata']['source']
        else:
            source_id = chunk['id'].split('-')[0]  # Extract filename from chunk ID
            
        if source_id not in sources:
            sources.append(source_id)
    
    context = "\n\n".join(context_parts)
    
    # Create prompt
    prompt = f"""
    Answer the following question based ONLY on the provided context. If the answer cannot be determined from the context, say "I don't have enough information to answer this question.
    Don't use phrases like "based on the provided context" or "based on the information provided" in your answer."
    
    Context:
    {context}
    
    Question: {question}
    
    """
    
    # Generate response using OpenAI
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about diabetes and nutrition based only on the provided context. You provide accurate, evidence-based information and clearly indicate when information is not available in the provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    # Prepare chunks for response
    response_chunks = []
    for chunk, score in relevant_chunks:
        if score >= 0.7 or relevant_chunks.index((chunk, score)) < 2:
            response_chunks.append({
                "text": chunk["text"],
                "id": chunk["id"],
                "score": score,
                "source": chunk.get("metadata", {}).get("source", chunk["id"].split('-')[0])
            })
    
    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
        "chunks": response_chunks
    }
