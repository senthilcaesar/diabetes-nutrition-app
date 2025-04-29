FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with specific versions to avoid compatibility issues
# Pin Streamlit to version 1.44.0 to avoid selectbox widget issues
RUN pip install --no-cache-dir streamlit==1.44.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set up a volume for persistent data
VOLUME ["/app/rag/chroma_db", "/app/rag/data"]

# Command to run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
