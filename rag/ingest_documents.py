"""
Script to ingest PDF documents from the data directory into Pinecone vector database.

This script should be run before using the RAG Q&A system to ensure the knowledge base
is up to date with the latest documents.
"""

import os
import pathlib
import sys
import argparse
from typing import List
import logging

from pinecone_utils import ingest_documents, delete_index

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_pdf_files(directory: str) -> List[str]:
    """
    Get all PDF files in a directory.
    
    Args:
        directory: Directory to search for PDF files
        
    Returns:
        List of paths to PDF files
    """
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files

def main():
    """
    Main function to ingest documents from the data directory.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Ingest documents into Pinecone vector database")
    parser.add_argument("--data_dir", type=str, default="./data", help="Directory containing PDF files")
    parser.add_argument("--index_name", type=str, default="diabetes-nutrition", help="Name of the Pinecone index")
    parser.add_argument("--reset", action="store_true", help="Delete existing index before ingestion")
    
    args = parser.parse_args()
    
    # Get the data directory path
    if os.path.isabs(args.data_dir):
        data_dir = args.data_dir
    else:
        data_dir = os.path.join(os.path.dirname(__file__), args.data_dir)
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        logger.error(f"Error: Data directory not found at {data_dir}")
        return
    
    # Get list of PDF files in the data directory
    pdf_files = get_pdf_files(data_dir)
    
    if not pdf_files:
        logger.error(f"No PDF files found in {data_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files: {', '.join(os.path.basename(f) for f in pdf_files)}")
    
    # Reset index if requested
    if args.reset:
        logger.info(f"Deleting existing index: {args.index_name}")
        delete_index(args.index_name)
    
    # Ingest documents
    try:
        num_chunks = ingest_documents(pdf_files, args.index_name)
        logger.info(f"Successfully ingested {num_chunks} document chunks into Pinecone index: {args.index_name}")
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        return

if __name__ == "__main__":
    main()
