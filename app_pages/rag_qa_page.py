"""
RAG Q&A page for the Diabetes Nutrition App.
This page provides a user interface for asking questions about diabetes and nutrition,
with answers retrieved from PDF documents using a RAG system with Pinecone.
"""

import os
import streamlit as st
from pathlib import Path

from utils.rag_system import find_similar_chunks, generate_response, ingest_documents
from rag.pinecone_utils import initialize_pinecone, delete_index

def show_rag_qa_page():
    """Display the RAG Q&A interface."""
    # Add custom CSS to style the page similar to the input data page
    st.markdown("""
    <style>
    /* Style for the active tab (primary button) */
    .stButton button[kind="primary"] {
        background-color: #87CEEB !important; /* Sky blue */
        color: #333333 !important; /* Dark gray for text */
        border-color: #000000 !important; /* Black border */
        font-weight: 600 !important;
    }
    
    /* Hover effect for inactive tabs */
    .stButton button[kind="secondary"]:hover {
        background-color: #E5E4E2 !important; /* Very light blue on hover */
        color: #333333 !important; /* Dark gray for text */
        border-color: #000000 !important; /* Black border */
        font-weight: 600 !important;
    }
    
    /* Style for the form container */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Style for input fields */
    .stNumberInput > div, 
    .stSelectbox > div,
    .stMultiSelect > div,
    .stTextArea > div,
    .stTextInput > div {
        background-color: #f8f9fa !important;
        border-radius: 10px !important;
    }
    
    /* Style for input fields */
    .stNumberInput input,
    .stSelectbox input,
    .stMultiSelect input,
    .stTextArea textarea,
    .stTextInput input {
        background-color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px !important;
    }
    
    /* Style for labels */
    .stNumberInput label, 
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label,
    .stTextInput label {
        font-weight: 500 !important;
        color: #333 !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='font-size: 22px; font-family: inherit;'>Ask Questions About Diabetes & Nutrition</h4>", unsafe_allow_html=True)
    
    # Check if Pinecone is properly configured
    index_name = "diabetes-nutrition"
    pinecone_configured = True
    
    try:
        # Try to initialize Pinecone
        initialize_pinecone()
    except Exception as e:
        pinecone_configured = False
        st.error(f"Error connecting to Pinecone: {str(e)}")
        st.info("Please make sure PINECONE_API_KEY and PINECONE_ENVIRONMENT are set in your environment variables or .env file.")
        return
    
    # Check if documents have been ingested
    # First, try to check if the index exists and has documents
    index_exists = False
    try:
        # Try to query the index with a simple test query to see if it exists and has documents
        test_results = find_similar_chunks("test query", index_name, 1)
        index_exists = len(test_results) > 0
    except Exception as e:
        # If there's an error, the index might not exist or be empty
        index_exists = False
        
    # Update session state based on the check
    if index_exists:
        st.session_state.pinecone_index_initialized = True
    elif "pinecone_index_initialized" not in st.session_state:
        st.session_state.pinecone_index_initialized = False
        
    # If the index is not initialized, show the warning and ingest button
    if not st.session_state.get("pinecone_index_initialized", False):
        st.warning("The knowledge base has not been created yet. Please ingest documents first.")
        
        if st.button("Ingest Documents"):
            with st.spinner("Processing documents... This may take a few minutes."):
                try:
                    # Get the data directory path
                    data_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "rag" / "data"
                    
                    # Ingest documents
                    num_chunks = ingest_documents(str(data_dir))
                    
                    st.success(f"Successfully processed documents and created {num_chunks} chunks!")
                    st.session_state.pinecone_index_initialized = True
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error ingesting documents: {str(e)}")
        
        # Show information about the ingestion process
        with st.expander("About Document Ingestion"):
            st.markdown("""
            The document ingestion process:
            1. Extracts text from PDF files in the data directory
            2. Splits the text into smaller chunks
            3. Generates embeddings for each chunk
            4. Stores the chunks with embeddings in a Pinecone index
            
            This process only needs to be run once, or when new documents are added to the data directory.
            """)
        
        return
    
    # Create a container for the main content
    main_container = st.container()
    
    # History management
    if "rag_history" not in st.session_state:
        st.session_state.rag_history = []
    
    with main_container:
        # Create a container with a light background and rounded corners
        with st.container():
            # Question input
            question = st.text_input("Enter your question:", 
                                    placeholder="e.g., What is the impact of exercise on glucose?",
                                    value=st.session_state.get("current_question", ""))
            
            # Clear current question after using it
            if "current_question" in st.session_state:
                del st.session_state.current_question
            
            # Create a column layout for the button (left-aligned)
            col1, col2 = st.columns([1, 3])
            with col1:
                # Process question when submitted
                submit_button = st.button("Get Answer", type="secondary", use_container_width=True)
        
        # Process the question when submitted
        if submit_button and question:
            with st.spinner("Searching for information..."):
                try:
                    # Find relevant chunks using Pinecone with question improvement
                    relevant_chunks, question_info = find_similar_chunks(question, index_name)
                    
                    # Generate response
                    response_data = generate_response(question, relevant_chunks, question_info)
                    
                    # Question processing information is now logged to the command line instead of displayed in the UI
                    
                    # Create a container for the answer with a light background
                    with st.container():
                        st.markdown("### Answer")
                        st.markdown(response_data["answer"])
                    
                    # Add to history (keep last 10 questions)
                    st.session_state.rag_history.insert(0, (question, response_data["answer"]))
                    if len(st.session_state.rag_history) > 10:
                        st.session_state.rag_history.pop()
                
                except Exception as e:
                    st.error(f"Error processing question: {str(e)}")
        
        with st.expander("About this Q&A System"):
            st.markdown("""This Q&A system uses Retrieval-Augmented Generation (RAG) with Pinecone vector database to answer your questions about diabetes and nutrition. All information comes from verified medical sources in our database.""")

            st.markdown("<h5 style='color:#20a7db; margin-top:0; border-bottom:2px solid #D3D3D3; padding-bottom:10px;'>Example Questions</h5>", unsafe_allow_html=True)
                               
            st.markdown("""
            - What is insulin?
            - What is insulin resistance?
            - What are normal blood glucose levels?
            - How does sleep affect glucose levels?
            - What is the root cause of Type 2 diabetes?
            - How does fiber affect blood glucose levels?
            - How does insulin affect blood glucose levels?
            - How does exercise affect blood glucose levels?
            - What's the best breakfast for stable glucose levels?
            - What is glucose and why is it important for the body?
            - How do glucose spikes affect energy levels and mood?
            - What's the relationship between glucose and heart health?
            - What's the connection between glucose and inflammation?
            - What's the relationship between carbohydrates and glucose?
            - What's the connection between glucose levels and diabetes?
            - What is the link between glucose spikes and inflammatory conditions?
            - How might I modify my breakfast to reduce morning glucose spikes?
            - What are the best strategies to prevent glucose spikes after meals?
            - What are the main differences between Type 1 and Type 2 diabetes?
            - What's the difference between glucose, fructose, and sucrose?
            - How does eating food in the right order help with glucose management?
                    """)   
    
    # Admin section for reingesting documents
    # with st.expander("Admin Options"):
    #     if st.button("Reingest Documents"):
    #         with st.spinner("Reprocessing documents... This may take a few minutes."):
    #             try:
    #                 # Delete existing index
    #                 delete_index(index_name)
                    
    #                 # Get the data directory path
    #                 data_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "rag" / "data"
                    
    #                 # Ingest documents
    #                 num_chunks = ingest_documents(str(data_dir))
                    
    #                 st.success(f"Successfully reprocessed documents and created {num_chunks} chunks!")
    #             except Exception as e:
    #                 st.error(f"Error ingesting documents: {str(e)}")
