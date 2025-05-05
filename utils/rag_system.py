"""
RAG (Retrieval-Augmented Generation) system for the Diabetes Nutrition App.
This module provides functions for retrieving relevant information from PDF documents
and generating responses to user questions using Pinecone for vector storage and retrieval.
"""

import os
import pathlib
import logging
from typing import List, Dict, Any, Tuple, Optional, Union

import streamlit as st
from openai import OpenAI

from rag.pinecone_utils import similarity_search, ingest_documents as pinecone_ingest_documents

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def improve_question(question: str, model: str = "gpt-4o") -> Dict[str, str]:
    """
    Improve a user question using LLM to enhance retrieval performance.
    If the question is already grammatically correct and understandable, it will not be improved.
    
    Args:
        question: Original user question
        model: OpenAI model to use for question improvement
        
    Returns:
        Dictionary containing the improved question and explanation
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=get_openai_api_key())
    
    # Create prompt for question improvement
    prompt = f"""
    You are an AI assistant. Your task is to evaluate and potentially improve the following question
    to make it more effective for retrieving relevant information from a knowledge base.
    
    Original Question: {question}
    
    First, evaluate if the question is already grammatically correct and understandable:
    - If the question is already well-formed, clear, and specific, DO NOT modify it. Return the original question unchanged.
    - If the question needs improvement, then proceed with the improvements below.
    
    Potential improvements (only if needed):
    1. Correct any grammar or spelling errors
    2. Make the question simple and easy to understand
    3. Ensure the question is clear
    4. Preserve the original intent of the question
    
    Return your response in the following format:
    Improved Question: [Your improved version of the question or the original if no improvement needed]
    Explanation: [Brief explanation of how you improved the question or why no improvement was needed]
    """
    
    # Generate improved question using OpenAI
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that improves questions to enhance information retrieval."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    # Extract improved question and explanation from response
    response_text = response.choices[0].message.content
    
    # Parse the response to extract improved question and explanation
    improved_question = ""
    explanation = ""
    
    for line in response_text.split('\n'):
        if line.startswith("Improved Question:"):
            improved_question = line.replace("Improved Question:", "").strip()
        elif line.startswith("Explanation:"):
            explanation = line.replace("Explanation:", "").strip()
    
    # If parsing failed or if the improved question is identical to the original, use the original question
    if not improved_question or improved_question.strip() == question.strip():
        improved_question = question
        if not explanation:
            explanation = "The original question is already clear and well-formed. No improvements needed."
    
    return {
        "original_question": question,
        "improved_question": improved_question,
        "explanation": explanation
    }

def find_similar_chunks(question: str, index_name: str = "diabetes-nutrition", top_k: int = 5, improve: bool = True) -> Tuple[List[Tuple[Dict[str, Any], float]], Dict[str, str]]:
    """
    Find chunks most similar to the question using Pinecone's similarity search.
    Optionally improves the question using LLM before searching.
    
    Args:
        question: User question
        index_name: Name of the Pinecone index
        top_k: Number of most similar chunks to return
        improve: Whether to improve the question using LLM
        
    Returns:
        Tuple containing:
        - List of tuples containing chunks and their similarity scores
        - Dictionary with question improvement information
    """
    # Improve question if requested
    question_info = {}
    search_question = question
    
    if improve:
        question_info = improve_question(question)
        search_question = question_info.get("improved_question", question)
        
        # Log question improvement information to command line
        logger.info(f"Question Processing:")
        logger.info(f"Original Question: {question_info.get('original_question', question)}")
        logger.info(f"Improved Question: {question_info.get('improved_question', search_question)}")
        logger.info(f"Explanation: {question_info.get('explanation', 'No explanation available.')}")
    
    # Query Pinecone for similar chunks
    results = similarity_search(search_question, index_name, top_k)
    
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
    
    return similar_chunks, question_info

def generate_response(question: str, relevant_chunks: List[Tuple[Dict[str, Any], float]], 
                     question_info: Dict[str, str] = None, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Generate a response using the question and relevant chunks as context.
    
    Args:
        question: User question
        relevant_chunks: List of tuples containing relevant chunks and their similarity scores
        question_info: Dictionary containing question improvement information
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
    
    # Determine which question to use in the prompt
    prompt_question = question
    if question_info and "improved_question" in question_info:
        prompt_question = question_info["improved_question"]
    
    # Create prompt
    prompt = f"""
    Answer the following question based ONLY on the provided context. If the answer cannot be determined from the context, say "I don't have enough information to answer this question.
    Don't use phrases like "based on the provided context" or "mentioned in the context" or "based on the information provided" in your answer."
    
    Context:
    {context}
    
    Question: {prompt_question}
    
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
        "chunks": response_chunks,
        "question_info": question_info
    }
