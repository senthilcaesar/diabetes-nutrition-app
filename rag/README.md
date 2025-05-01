# Diabetes Nutrition App: RAG System with Pinecone

This document explains the Retrieval-Augmented Generation (RAG) system implemented for the Diabetes Nutrition App using Pinecone as the vector database. The system enables users to ask questions about diabetes and nutrition and receive accurate answers based on information extracted from medical literature.

## System Architecture

```mermaid
graph TD
    A[PDF Documents] -->|Extract Text| B[Text Extraction]
    B -->|Split into Chunks| C[Text Chunking]
    C -->|Generate Embeddings| D[Vector Embeddings]
    D -->|Store in Pinecone| E[Pinecone Vector Database]

    F[User Question] -->|Generate Embedding| G[Question Embedding]
    G -->|Query Pinecone| E
    E -->|Return Similar Chunks| H[Relevant Chunks]
    H -->|Context for LLM| I[OpenAI GPT Model]
    I -->|Generate Response| J[Answer to User]
```

## Document Ingestion Process

The document ingestion process transforms PDF documents into searchable vector embeddings stored in Pinecone. Here's how it works:

### 1. Text Extraction from PDFs

The system uses `pymupdf4llm` to extract text from PDF files:

```python
md_text = pymupdf4llm.to_markdown(file_path)
```

This converts PDF content to markdown format, preserving document structure while making it suitable for processing. The extraction handles various PDF elements including:

- Text content
- Headers and formatting
- Tables (converted to markdown format)
- Lists and bullet points

### 2. Text Chunking

The extracted text is split into smaller, manageable chunks using LangChain's `RecursiveCharacterTextSplitter`:

```python
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-4o", chunk_size=500, chunk_overlap=125
)
texts = text_splitter.create_documents([md_text])
```

Key chunking parameters:

- **Chunk Size**: 500 characters per chunk
- **Chunk Overlap**: 125 characters overlap between consecutive chunks
- **Tokenizer**: Uses tiktoken with the gpt-4o model for accurate token counting

The overlap ensures that context isn't lost between chunks, which is crucial for maintaining coherence when retrieving information that might span chunk boundaries.

### 3. Embedding Generation

For each text chunk, the system generates a vector embedding using OpenAI's embedding model:

```python
embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
).data[0].embedding
```

These embeddings are dense vector representations (1536 dimensions) that capture the semantic meaning of each text chunk, enabling semantic search rather than just keyword matching.

### 4. Storage in Pinecone

The embeddings, along with their corresponding text and metadata, are stored in a Pinecone vector database:

```python
vector = {
    "id": chunk["id"],
    "values": embedding,
    "metadata": metadata
}
index.upsert(vectors=vectors)
```

Each vector in Pinecone contains:

- **ID**: A unique identifier (e.g., "Diabetes_Code.pdf-42")
- **Values**: The 1536-dimensional embedding vector
- **Metadata**:
  - Source document name
  - Chunk position in the document
  - The original text content
  - Other relevant information

The vectors are stored in batches (100 vectors per batch) to optimize the ingestion process.

## Pinecone Configuration

The system uses Pinecone's serverless configuration for the vector database:

```python
spec = {
    "dimension": 1536,
    "metric": "cosine",
    "serverless": {
        "cloud": "aws",
        "region": "us-east-1"
    }
}
```

Key configuration parameters:

- **Dimension**: 1536 (matching OpenAI's text-embedding-3-small model)
- **Metric**: Cosine similarity for measuring vector distances
- **Cloud Provider**: AWS
- **Region**: us-east-1 (compatible with free tier)

## Query and Retrieval Process

When a user asks a question, the system follows these steps to retrieve relevant information and generate a response:

### 1. Question Embedding

The user's question is converted into a vector embedding using the same OpenAI embedding model:

```python
query_embedding = generate_embedding(query)
```

### 2. Similarity Search

The question embedding is used to query the Pinecone index for similar chunks:

```python
results = index.query(
    vector=query_embedding,
    top_k=top_k,
    include_metadata=True
)
```

Pinecone performs a similarity search using cosine similarity to find the chunks most semantically related to the question. The system retrieves the top-k most similar chunks (default: 5).

### 3. Context Assembly

The retrieved chunks are assembled into a context for the language model:

```python
for i, (chunk, score) in enumerate(relevant_chunks):
    # Only include chunks with similarity above a threshold
    if score < 0.7 and i >= 2:  # Include at least 2 chunks regardless of score
        continue
    context_parts.append(f"[{i+1}] {chunk['text']}")
```

The system:

- Includes chunks with similarity scores above 0.7
- Always includes at least the top 2 chunks regardless of score
- Formats the context with chunk numbers for reference

### 4. Response Generation

The assembled context and the original question are sent to OpenAI's GPT model to generate a response:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant..."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)
```

The system uses a low temperature (0.3) to ensure factual, consistent responses based on the provided context.

## Using the RAG System

### Command Line Ingestion

You can ingest documents using the command line:

```bash
python rag/ingest_documents.py
```

Optional arguments:

- `--data_dir`: Directory containing PDF files (default: "./data")
- `--index_name`: Name of the Pinecone index (default: "diabetes-nutrition")
- `--reset`: Delete existing index before ingestion

### Web Interface

The system is integrated into the Streamlit web app:

1. Navigate to the "Q&A" tab
2. The system automatically detects if documents have been ingested
3. If not, you can click "Ingest Documents" to process the PDFs
4. Once documents are ingested, you can ask questions in the text input field
5. Click "Get Answer" to receive a response based on the ingested documents

## Environment Setup

The system requires the following environment variables:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

These can be set in a `.env` file in the project root directory.

## Technical Requirements

- **Python 3.8+**
- **Dependencies**:
  - pinecone (v6.0.2+)
  - openai
  - pymupdf4llm
  - langchain_text_splitters
  - python-dotenv
  - streamlit (for web interface)

## Troubleshooting

### Common Issues

1. **Pinecone Connection Errors**:

   - Verify your API key and environment variables
   - Check if your Pinecone account is active
   - Ensure you're using a supported region for your account tier

2. **OpenAI API Errors**:

   - Verify your OpenAI API key
   - Check if you have sufficient API credits
   - Ensure you're not exceeding rate limits

3. **Document Ingestion Issues**:

   - Verify PDF files are in the correct directory
   - Check if PDFs are readable and not corrupted
   - Ensure you have sufficient permissions to read the files

4. **Query Issues**:
   - If responses are generic, try rephrasing your question
   - If responses mention missing information, your question might be outside the scope of ingested documents
   - For better results, ask specific questions related to diabetes and nutrition

## Performance Optimization

- **Chunk Size**: Adjust chunk size based on your content. Smaller chunks (300-500 characters) work well for precise retrieval, while larger chunks provide more context.
- **Embedding Model**: The system uses OpenAI's text-embedding-3-small model for a good balance of quality and cost. For higher accuracy, consider using text-embedding-3-large.
- **Similarity Threshold**: Adjust the 0.7 threshold based on your needs. Lower thresholds include more context but might introduce noise.
- **Batch Size**: The default batch size of 100 vectors works well for most cases. For very large documents, consider adjusting this value.

## Security Considerations

- API keys are stored in environment variables or .env files, not hardcoded
- User queries are processed locally before being sent to OpenAI
- Document content is stored in your private Pinecone index
- No user data is shared between different users of the system
