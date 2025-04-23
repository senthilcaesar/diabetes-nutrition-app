"""
RAG (Retrieval-Augmented Generation) system for the Diabetes Nutrition App.
This module provides functions for retrieving relevant information from PDF documents
and generating responses to user questions.
"""

import json
import numpy as np
import os
import pathlib
from typing import List, Dict, Any, Tuple

import streamlit as st
import openai
from openai import OpenAI
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score between 0 and 1
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def ingest_documents(data_dir: str, output_file: str = "rag_ingested_chunks.json") -> None:
    """
    Process PDF documents in the data directory, extract text, split into chunks,
    generate embeddings, and save to a JSON file.
    
    Args:
        data_dir: Path to directory containing PDF files
        output_file: Path to output JSON file
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Get list of PDF files in the data directory
    data_path = pathlib.Path(data_dir)
    filenames = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
    
    all_chunks = []
    for filename in filenames:
        # Extract text from the PDF file
        md_text = pymupdf4llm.to_markdown(data_path / filename)

        # Split the text into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4o", chunk_size=500, chunk_overlap=125
        )
        texts = text_splitter.create_documents([md_text])
        file_chunks = [{"id": f"{filename}-{(i + 1)}", "text": text.page_content} for i, text in enumerate(texts)]

        # Generate embeddings using openAI SDK for each text
        for file_chunk in file_chunks:
            file_chunk["embedding"] = (
                client.embeddings.create(model="text-embedding-3-small", input=file_chunk["text"]).data[0].embedding
            )
        all_chunks.extend(file_chunks)

    # Save the documents with embeddings to a JSON file
    with open(output_file, "w") as f:
        json.dump(all_chunks, f, indent=4)
    
    return len(all_chunks)

def load_chunks(file_path: str = "rag_ingested_chunks.json") -> List[Dict[str, Any]]:
    """
    Load preprocessed chunks from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing chunks with embeddings
        
    Returns:
        List of chunks with text and embeddings
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Chunks file not found at {file_path}. Run ingest_documents first.")

def find_similar_chunks(question: str, all_chunks: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Find chunks most similar to the question using cosine similarity.
    
    Args:
        question: User question
        all_chunks: List of chunks with text and embeddings
        top_k: Number of most similar chunks to return
        
    Returns:
        List of most similar chunks
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Generate embedding for the question
    question_embedding = client.embeddings.create(
        model="text-embedding-3-small", 
        input=question
    ).data[0].embedding
    
    # Calculate similarity scores
    similarities = []
    for chunk in all_chunks:
        similarity = cosine_similarity(question_embedding, chunk["embedding"])
        similarities.append((chunk, similarity))
    
    # Sort by similarity score and return top_k
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [(item[0], item[1]) for item in similarities[:top_k]]

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
    
    # Extract chunks and scores
    chunks = [chunk for chunk, _ in relevant_chunks]
    scores = [score for _, score in relevant_chunks]
    
    # Create context from relevant chunks
    context_parts = []
    sources = []
    
    for i, (chunk, score) in enumerate(relevant_chunks):
        # Only include chunks with similarity above a threshold
        if score < 0.7 and i >= 2:  # Include at least 2 chunks regardless of score
            continue
            
        context_parts.append(f"[{i+1}] {chunk['text']}")
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
    
    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
        "chunks": [{"text": chunk["text"], "id": chunk["id"], "score": score} for chunk, score in relevant_chunks if score >= 0.7 or relevant_chunks.index((chunk, score)) < 2]
    }
