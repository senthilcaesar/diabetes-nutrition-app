"""
RAG (Retrieval-Augmented Generation) system for the Diabetes Nutrition App.
This module provides functions for retrieving relevant information from PDF documents
and generating responses to user questions using ChromaDB for vector storage and retrieval.
"""

import numpy as np
import os
import pathlib
from typing import List, Dict, Any, Tuple, Optional, Union

import streamlit as st
import openai
from openai import OpenAI
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings

def get_chroma_client():
    """
    Initialize and return a ChromaDB client with persistent storage.
    Uses session state to ensure the same client is used throughout the application.
    
    Returns:
        chromadb.Client: Initialized ChromaDB client
    """
    # Use Streamlit session state to store the client instance
    # This ensures we use the same client throughout the application
    if "chroma_client" not in st.session_state:
        # Create a directory for ChromaDB if it doesn't exist
        chroma_dir = pathlib.Path(os.path.dirname(os.path.dirname(__file__))) / "rag" / "chroma_db"
        os.makedirs(chroma_dir, exist_ok=True)
        
        # Create a persistent client
        st.session_state.chroma_client = chromadb.PersistentClient(path=str(chroma_dir))
    
    return st.session_state.chroma_client

def ingest_documents(data_dir: str, collection_name: str = "diabetes_nutrition_docs") -> int:
    """
    Process PDF documents in the data directory, extract text, split into chunks,
    generate embeddings, and store in a ChromaDB collection.
    
    Args:
        data_dir: Path to directory containing PDF files
        collection_name: Name of the ChromaDB collection to store documents
        
    Returns:
        int: Number of chunks added to the collection
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Initialize ChromaDB client
    chroma_client = get_chroma_client()
    
    # Check if collection exists and delete it to start fresh
    try:
        existing_collections = chroma_client.list_collections()
        if any(collection.name == collection_name for collection in existing_collections):
            chroma_client.delete_collection(collection_name)
    except Exception as e:
        print(f"Error checking existing collections: {str(e)}")
    
    # Create a new collection
    collection = chroma_client.create_collection(
        name=collection_name,
        metadata={"description": "Diabetes and nutrition documents"}
    )
    
    # Get list of PDF files in the data directory
    data_path = pathlib.Path(data_dir)
    filenames = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
    
    total_chunks_added = 0
    for filename in filenames:
        # Extract text from the PDF file
        md_text = pymupdf4llm.to_markdown(data_path / filename)

        # Split the text into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4o", chunk_size=500, chunk_overlap=125
        )
        texts = text_splitter.create_documents([md_text])
        
        # Prepare data for ChromaDB
        chunk_ids = []
        chunk_texts = []
        chunk_embeddings = []
        chunk_metadatas = []
        
        # Generate embeddings for each chunk and prepare for ChromaDB
        for i, text in enumerate(texts):
            chunk_id = f"{filename}-{(i + 1)}"
            
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
        
        # Add chunks to ChromaDB collection
        if chunk_ids:
            collection.add(
                ids=chunk_ids,
                documents=chunk_texts,
                embeddings=chunk_embeddings,
                metadatas=chunk_metadatas
            )
            total_chunks_added += len(chunk_ids)
    
    return total_chunks_added

def load_chunks(collection_name: str = "diabetes_nutrition_docs") -> chromadb.Collection:
    """
    Load the ChromaDB collection containing preprocessed chunks.
    
    Args:
        collection_name: Name of the ChromaDB collection
        
    Returns:
        chromadb.Collection: ChromaDB collection containing chunks with embeddings
    """
    try:
        chroma_client = get_chroma_client()
        collection = chroma_client.get_collection(collection_name)
        return collection
    except Exception as e:
        raise ValueError(f"ChromaDB collection '{collection_name}' not found. Run ingest_documents first. Error: {str(e)}")

def find_similar_chunks(question: str, collection: chromadb.Collection, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
    """
    Find chunks most similar to the question using ChromaDB's similarity search.
    
    Args:
        question: User question
        collection: ChromaDB collection containing chunks with embeddings
        top_k: Number of most similar chunks to return
        
    Returns:
        List of tuples containing chunks and their similarity scores
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Generate embedding for the question
    question_embedding = client.embeddings.create(
        model="text-embedding-3-small", 
        input=question
    ).data[0].embedding
    
    # Query ChromaDB for similar chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    # Format results as list of tuples (chunk, similarity)
    similar_chunks = []
    for i in range(len(results["ids"][0])):
        chunk_id = results["ids"][0][i]
        document = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        # Convert distance to similarity score (ChromaDB returns L2 distance, lower is better)
        # We'll convert to a similarity score between 0 and 1 where higher is better
        distance = results["distances"][0][i]
        similarity = 1.0 / (1.0 + distance)  # Convert distance to similarity
        
        chunk = {
            "id": chunk_id,
            "text": document,
            "metadata": metadata
        }
        
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
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
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
    Answer the following question based ONLY on the provided context. If the answer cannot be determined from the context, say "I don't have enough information to answer this question based on the available documents."
    
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
