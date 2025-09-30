## Vertex AI RAG Agent (Google ADK)

This project implements a fully functional Retrieval-Augmented Generation (RAG) agent using the Google Agent Development Kit (ADK) on Vertex AI. The agent can create, manage, and query document corpora using Vertex AI's RAG capabilities.

### Prerequisites
- Google Cloud project with billing enabled
- Vertex AI API enabled (`aiplatform.googleapis.com`)
- Authenticated locally via:
  - `gcloud init`
  - `gcloud auth application-default login`

### Tech Stack
- **Google ADK** (`google-adk>=0.5.0`) - Agent Development Kit for building AI agents
- **Vertex AI SDK** (`google-cloud-aiplatform>=1.92.0`) - Core Vertex AI functionality
- **Google Cloud Storage** (`google-cloud-storage>=2.19.0`) - For document storage and retrieval
- **Google GenAI** (`google-genai>=1.14.0`) - Gemini model integration
- **GitPython** (`gitpython>=3.1.40`) - Git repository management for data ingestion

### Setup
1. **Environment Setup**: Use your existing Python environment
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Authentication**: Ensure you're authenticated with Google Cloud:
   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```
4. **Agent Configuration**: The agent is configured to use:
   - **Model**: `gemini-2.5-flash-lite`
   - **Embedding Model**: `publishers/google/models/text-embedding-005`
   - **Default Parameters**: 
     - Top K results: 3
     - Distance threshold: 0.5

### Available Tools

The RAG agent comes with six specialized tools for corpus management and querying:

#### 1. **create_corpus**
Creates a new document corpus with the specified name.
- **Parameters**: 
  - `corpus_name` (str): The name for the new corpus
- **Returns**: Status confirmation with corpus name

#### 2. **list_corpora**
Lists all available document corpora in your project.
- **Parameters**: None
- **Returns**: List of all corpora with their resource names

#### 3. **list_corpus_files**
Provides detailed information about files within a specific corpus.
- **Parameters**:
  - `corpus_name` (str): The name of the corpus to inspect
- **Returns**: List of files and their details in the specified corpus

#### 4. **upload_data**
Uploads new documents to an existing corpus.
- **Parameters**:
  - `corpus_name` (str): The name of the corpus to add data to
- **Returns**: Upload status and confirmation

#### 5. **rag_query**
Queries a corpus to answer questions using semantic search.
- **Parameters**:
  - `corpus_name` (str): The name of the corpus to query
  - `query` (str): The text question to ask
- **Returns**: Relevant document chunks with scores and source information
- **Configuration**: Uses top-k=3 and distance threshold=0.5 by default

#### 6. **delete_corpus**
Deletes an entire corpus and all its associated files.
- **Parameters**:
  - `corpus_name` (str): The name of the corpus to delete
  - `confirm` (bool): Must be set to True to confirm deletion
- **Returns**: Deletion confirmation

### References
- ADK documentation: `https://google.github.io/adk-docs/`
- ADK samples: `https://github.com/google/adk-samples`

### Project Structure

```
rag_agent/
├── __init__.py              # Package initialization
├── agent.py                 # Main agent configuration
├── prompts.py               # Agent prompts and instructions
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
└── tools/                  # Tool implementations
    ├── __init__.py         # Tools package initialization
    ├── create_corpus.py    # Corpus creation tool
    ├── delete_corpus.py    # Corpus deletion tool
    ├── list_corpora.py     # List all corpora tool
    ├── list_corpus_files.py # List corpus files tool
    ├── rag_query.py        # Query corpus tool
    └── upload_data.py      # Data upload tool
```

### Agent Configuration

The agent is configured with the following specifications:
- **Name**: `rag_agent`
- **Model**: `gemini-2.5-flash-lite`
- **Description**: "RAG agent using vertex ai"
- **Tools**: All six corpus management and querying tools
- **Instructions**: Comprehensive prompt for RAG operations


