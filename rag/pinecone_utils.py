"""
Pinecone utility functions for the Diabetes Nutrition App RAG system.
Handles initialization, indexing, and querying operations for Pinecone vector database.
"""

import os
import pinecone
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import uuid
import logging
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import streamlit for secrets, but don't fail if not available
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

def initialize_pinecone():
    """
    Initialize Pinecone client with API key and environment.
    First tries to get credentials from Streamlit secrets, then falls back to environment variables.
    
    Returns:
        pinecone.Pinecone: Initialized Pinecone client
    """
    # Load environment variables
    load_dotenv()
    
    # Try to get credentials from Streamlit secrets first
    api_key = None
    environment = None
    
    # Check if Streamlit is available
    if STREAMLIT_AVAILABLE:
        try:
            # Access Streamlit secrets using dictionary-like syntax
            api_key = st.secrets["PINECONE_API_KEY"]
            environment = st.secrets["PINECONE_ENVIRONMENT"]
            logger.info("Successfully loaded Pinecone credentials from Streamlit secrets")
        except Exception as e:
            logger.warning(f"Could not get Pinecone credentials from Streamlit secrets: {str(e)}")
    
    # Fall back to environment variables if not found in Streamlit secrets
    if not api_key:
        api_key = os.environ.get("PINECONE_API_KEY")
    
    if not environment:
        environment = os.environ.get("PINECONE_ENVIRONMENT")
    
    if not api_key or not environment:
        raise ValueError("Pinecone API key and environment must be set in Streamlit secrets or environment variables")
    
    return pinecone.Pinecone(api_key=api_key, environment=environment)

def get_or_create_index(pc, index_name: str, dimension: int = 1536, metric: str = "cosine"):
    """
    Get existing index or create a new one if it doesn't exist.
    
    Args:
        pc: Pinecone client
        index_name: Name of the index
        dimension: Vector dimension (1536 for text-embedding-3-small)
        metric: Distance metric for similarity search
        
    Returns:
        pinecone.Index: Pinecone index
    """
    # Check if index already exists
    existing_indexes = pc.list_indexes()
    
    if not hasattr(existing_indexes, 'names'):
        # For newer Pinecone versions, the list_indexes() might return a different structure
        existing_index_names = [idx.name for idx in existing_indexes]
    else:
        existing_index_names = existing_indexes.names()
    
    if index_name not in existing_index_names:
        try:
            # Try creating with the newer API format
            from pinecone import ServerlessSpec
            
            # Create a serverless spec
            spec = ServerlessSpec(
                cloud="aws",
                region="us-east-1"  # Using us-east-1 which is typically supported in free plans
            )
            
            # Create the index with the spec parameter
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=spec
            )
            logger.info(f"Created new Pinecone index: {index_name}")
        except (ImportError, AttributeError, TypeError) as e:
            logger.warning(f"Error using ServerlessSpec: {str(e)}")
            
            # Fallback to direct dictionary approach
            try:
                spec = {
                    "dimension": dimension,
                    "metric": metric,
                    "serverless": {
                        "cloud": "aws",
                        "region": "us-east-1"
                    }
                }
                
                # Create the index with the spec parameter
                pc.create_index(
                    name=index_name,
                    spec=spec
                )
                logger.info(f"Created new Pinecone index using fallback method: {index_name}")
            except Exception as e2:
                logger.error(f"Failed to create index with fallback method: {str(e2)}")
                raise
    else:
        logger.info(f"Using existing Pinecone index: {index_name}")
    
    # Connect to index
    return pc.Index(index_name)

def delete_all_vectors(index):
    """
    Delete all vectors from the index.
    
    Args:
        index: Pinecone index
    """
    index.delete(delete_all=True)

def format_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format metadata to be compatible with Pinecone.
    Pinecone only supports string, number, and boolean values in metadata.
    
    Args:
        metadata: Original metadata dictionary
        
    Returns:
        Dict[str, Any]: Formatted metadata
    """
    formatted = {}
    for key, value in metadata.items():
        # Convert all values to strings except numbers and booleans
        if not isinstance(value, (int, float, bool)):
            formatted[key] = str(value)
        else:
            formatted[key] = value
    return formatted

def get_openai_api_key():
    """
    Get the OpenAI API key from Streamlit secrets, environment variables, or user input.
    First tries Streamlit secrets, then falls back to environment variables.
    
    Returns:
        str: OpenAI API key
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Try to get API key from Streamlit secrets first
    api_key = None
    
    if STREAMLIT_AVAILABLE:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
            logger.info("Successfully loaded OpenAI API key from Streamlit secrets")
        except Exception as e:
            logger.warning(f"Could not get OpenAI API key from Streamlit secrets: {str(e)}")
    
    # If not found in Streamlit secrets, try environment variables
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")
    
    # If still not found, prompt the user
    if not api_key:
        logger.error("OpenAI API key not found in Streamlit secrets or environment variables.")
        api_key = input("Please enter your OpenAI API key: ")
        
        if not api_key:
            raise ValueError("No API key provided.")
    
    return api_key

def generate_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate an embedding for a text using OpenAI's embedding model.
    
    Args:
        text: Text to generate embedding for
        model: OpenAI embedding model to use
        
    Returns:
        List[float]: Embedding vector
    """
    # Get OpenAI API key
    api_key = get_openai_api_key()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Generate embedding
    embedding = client.embeddings.create(
        model=model, 
        input=text
    ).data[0].embedding
    
    return embedding

def load_and_split_documents(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Load PDF documents, extract text, and split into chunks.
    
    Args:
        file_paths: List of paths to PDF files
        
    Returns:
        List of dictionaries containing chunk text and metadata
    """
    chunks = []
    
    # Text splitter for chunking documents
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o", chunk_size=500, chunk_overlap=125
    )
    
    for file_path in file_paths:
        try:
            logger.info(f"Processing {file_path}...")
            
            # Extract text from the PDF file
            md_text = pymupdf4llm.to_markdown(file_path)
            logger.info(f"  Extracted {len(md_text)} characters of text")
            
            # Split the text into smaller chunks
            texts = text_splitter.create_documents([md_text])
            logger.info(f"  Split into {len(texts)} chunks")
            
            # Extract filename for metadata
            filename = os.path.basename(file_path)
            
            # Process each chunk
            for i, text in enumerate(texts):
                chunks.append({
                    "id": f"{filename}-{i+1}",
                    "text": text.page_content,
                    "metadata": {
                        "source": filename,
                        "chunk_index": i + 1,
                        "total_chunks": len(texts)
                    }
                })
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
    
    return chunks

def ingest_documents(file_paths: List[str], index_name: str = "diabetes-nutrition") -> int:
    """
    Ingest documents into Pinecone.
    
    Args:
        file_paths: List of paths to PDF files
        index_name: Name of the Pinecone index
        
    Returns:
        Number of chunks ingested
    """
    # Initialize Pinecone
    pc = initialize_pinecone()
    
    # Get or create index
    index = get_or_create_index(pc, index_name)
    
    # Load and split documents
    chunks = load_and_split_documents(file_paths)
    
    if not chunks:
        logger.warning("No chunks to ingest")
        return 0
    
    # Process chunks in batches (Pinecone has a limit on batch size)
    batch_size = 100
    total_chunks_added = 0
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        
        # Prepare vectors for Pinecone
        vectors = []
        for chunk in batch:
            try:
                # Generate embedding
                embedding = generate_embedding(chunk["text"])
                
                # Format metadata
                metadata = format_metadata(chunk["metadata"])
                metadata["text"] = chunk["text"]  # Store the text in metadata for retrieval
                
                # Create vector
                vector = {
                    "id": chunk["id"],
                    "values": embedding,
                    "metadata": metadata
                }
                
                vectors.append(vector)
                
            except Exception as e:
                logger.error(f"Error generating embedding for chunk {chunk['id']}: {str(e)}")
        
        # Upsert vectors to Pinecone
        if vectors:
            try:
                index.upsert(vectors=vectors)
                logger.info(f"Added {len(vectors)} vectors to Pinecone")
                total_chunks_added += len(vectors)
            except Exception as e:
                logger.error(f"Error upserting vectors to Pinecone: {str(e)}")
    
    logger.info(f"Successfully added {total_chunks_added} chunks to Pinecone index '{index_name}'")
    return total_chunks_added

def similarity_search(query: str, index_name: str = "diabetes-nutrition", top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform similarity search on Pinecone index.
    
    Args:
        query: Query string
        index_name: Name of the Pinecone index
        top_k: Number of results to return
        
    Returns:
        List of dictionaries containing chunk text and metadata
    """
    # Initialize Pinecone
    pc = initialize_pinecone()
    
    # Get index
    index = pc.Index(index_name)
    
    # Generate embedding for query
    query_embedding = generate_embedding(query)
    
    # Query Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    # Format results
    formatted_results = []
    for match in results["matches"]:
        # Extract text and metadata
        metadata = match["metadata"]
        text = metadata.pop("text", "")  # Remove text from metadata and store separately
        
        # Calculate similarity score (convert distance to similarity)
        similarity = 1.0 - match["score"]  # Assuming cosine distance
        
        formatted_results.append({
            "id": match["id"],
            "text": text,
            "metadata": metadata,
            "score": similarity
        })
    
    return formatted_results

def delete_index(index_name: str = "diabetes-nutrition") -> bool:
    """
    Delete a Pinecone index.
    
    Args:
        index_name: Name of the Pinecone index
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Initialize Pinecone
        pc = initialize_pinecone()
        
        # Check if index exists
        existing_indexes = pc.list_indexes()
        
        if not hasattr(existing_indexes, 'names'):
            # For newer Pinecone versions, the list_indexes() might return a different structure
            existing_index_names = [idx.name for idx in existing_indexes]
        else:
            existing_index_names = existing_indexes.names()
        
        if index_name in existing_index_names:
            # Delete index
            pc.delete_index(index_name)
            logger.info(f"Deleted Pinecone index: {index_name}")
            return True
        else:
            logger.warning(f"Index {index_name} does not exist")
            return False
    except Exception as e:
        logger.error(f"Error deleting index {index_name}: {str(e)}")
        return False
