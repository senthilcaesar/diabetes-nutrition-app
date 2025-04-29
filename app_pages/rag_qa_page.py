"""
RAG Q&A page for the Diabetes Nutrition App.
This page provides a user interface for asking questions about diabetes and nutrition,
with answers retrieved from PDF documents using a RAG system with ChromaDB.
"""

import os
import streamlit as st
from pathlib import Path
import chromadb

from utils.rag_system import load_chunks, find_similar_chunks, generate_response, ingest_documents, get_chroma_client

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
    
    # Check if ChromaDB collection exists, if not, show option to ingest documents
    collection_name = "diabetes_nutrition_docs"
    chroma_client = get_chroma_client()
    
    # Check if collection exists
    try:
        existing_collections = chroma_client.list_collections()
        collection_exists = any(collection.name == collection_name for collection in existing_collections)
    except Exception:
        collection_exists = False
    
    if not collection_exists:
        st.warning("The knowledge base has not been created yet. Please ingest documents first.")
        
        if st.button("Ingest Documents"):
            with st.spinner("Processing documents... This may take a few minutes."):
                try:
                    # Get the data directory path
                    data_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "data"
                    
                    # Ingest documents
                    num_chunks = ingest_documents(str(data_dir))
                    
                    st.success(f"Successfully processed documents and created {num_chunks} chunks!")
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
            4. Stores the chunks with embeddings in a ChromaDB collection
            
            This process only needs to be run once, or when new documents are added to the data directory.
            """)
        
        return
    
    # Create a container for the main content
    main_container = st.container()
    
    # History management
    if "rag_history" not in st.session_state:
        st.session_state.rag_history = []
    
    # Show history in sidebar if there are previous questions
    # if st.session_state.rag_history:
    #     with st.sidebar:
    #         st.markdown("### Previous Questions")
    #         for i, (q, a) in enumerate(st.session_state.rag_history):
    #             if st.button(f"{q[:50]}{'...' if len(q) > 50 else ''}", key=f"history_{i}"):
    #                 st.session_state.current_question = q
    #                 st.experimental_rerun()
    
    with main_container:
        # Create a container with a light background and rounded corners
        with st.container():
            # Question input
            question = st.text_input("Enter your question:", 
                                    placeholder="e.g., What is glucose and why is it important for the body?",
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
                    # Load ChromaDB collection
                    collection = load_chunks(collection_name)
                    
                    # Find relevant chunks using ChromaDB
                    relevant_chunks = find_similar_chunks(question, collection)
                    
                    # Generate response
                    response_data = generate_response(question, relevant_chunks)
                    
                    # Create a container for the answer with a light background
                    with st.container():
                        st.markdown("### Answer")
                        st.markdown(response_data["answer"])
                    
                    # Add to history (keep last 10 questions)
                    st.session_state.rag_history.insert(0, (question, response_data["answer"]))
                    if len(st.session_state.rag_history) > 10:
                        st.session_state.rag_history.pop()
                    
                    # Show sources
                    # st.markdown("### Sources")
                    # st.markdown(f"Information retrieved from: {', '.join(response_data['sources'])}")
                    
                    # Show relevant chunks
                    # with st.expander("View Source Passages"):
                    #     for i, chunk in enumerate(response_data["chunks"]):
                    #         source = chunk.get('source', chunk['id'].split('-')[0])
                    #         st.markdown(f"**Passage {i+1}** (from {source})")
                    #         st.markdown(chunk["text"])
                    #         st.markdown(f"*Relevance score: {chunk['score']:.2f}*")
                    #         st.markdown("---")
                
                except Exception as e:
                    st.error(f"Error processing question: {str(e)}")
        
        # Information about the RAG system
        # How it works:
        # 1. Your question is converted into a numerical representation (embedding)
        # 2. The system finds the most relevant passages from our knowledge base
        # 3. These passages are used as context to generate an accurate answer

        with st.expander("About this Q&A System"):
            st.markdown("""
            This Q&A system uses Retrieval-Augmented Generation (RAG) to answer your questions about diabetes and nutrition.       
            All information comes from verified medical sources in our database.""")

            st.markdown("<h5 style='color:#20a7db; margin-top:0; border-bottom:2px solid #D3D3D3; padding-bottom:10px;'>Example Questions</h5>", unsafe_allow_html=True)
                               
            st.markdown("""
            - What is insulin?
            - What is insulin resistance?
            - What are normal blood glucose levels?
            - What is the root cause of Type 2 diabetes?
            - How does fiber affect blood glucose levels?
            - How does insulin affect blood glucose levels?
            - How does exercise affect blood glucose levels?
            - How do glucose levels affect cognitive function?
            - What's the best breakfast for stable glucose levels?
            - What is glucose and why is it important for the body?
            - How do glucose spikes affect energy levels and mood?
            - What's the relationship between glucose and heart health?
            - What's the connection between glucose and inflammation?
            - What's the relationship between carbohydrates and glucose?
            - What's the connection between glucose levels and diabetes?
            - What are the best strategies to prevent glucose spikes after meals?
            - What are the main differences between Type 1 and Type 2 diabetes?
            - How does eating food in the right order help with glucose management?
                    """)
            
            st.markdown("<h5 style='color:#20a7db; margin-top:0; border-bottom:2px solid #D3D3D3; padding-bottom:10px;'>Example Answer</h5>", unsafe_allow_html=True)
            
            st.markdown("""What is insulin resistance? Please explain in layman's terms.""")

            st.markdown("""Insulin resistance is a condition where the body's cells don't respond well to insulin, a hormone that helps control blood sugar levels. Imagine insulin as a key that opens a door to let glucose (sugar) into the cells for energy. In insulin resistance, 
                        the key (insulin) doesn't fit the lock (the cell's receptor) very well, so the door doesn't open easily. As a result, glucose builds up in the blood instead of entering the cells. The body tries to compensate by producing more insulin, but this can lead to problems like high blood sugar and excessive fat in the liver.
                        """)       
    
    # Admin section for reingesting documents
    # with st.expander("Admin Options"):
    #     if st.button("Reingest Documents"):
    #         with st.spinner("Reprocessing documents... This may take a few minutes."):
    #             try:
    #                 # Get the data directory path
    #                 data_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "data"
                    
    #                 # Ingest documents
    #                 num_chunks = ingest_documents(str(data_dir))
                    
    #                 st.success(f"Successfully reprocessed documents and created {num_chunks} chunks!")
    #             except Exception as e:
    #                 st.error(f"Error ingesting documents: {str(e)}")
