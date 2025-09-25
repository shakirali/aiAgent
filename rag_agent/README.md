## Vertex AI RAG Agent (Google ADK)

This project will implement a Retrieval-Augmented Generation (RAG) agent using the Google Agent Development Kit (ADK) on Vertex AI.

We will proceed step by step, starting with environment setup and dependencies, then scaffolding the agent and adding RAG tools (create/list/info/delete corpora, ingest data, and query).

### Prerequisites
- Google Cloud project with billing enabled
- Vertex AI API enabled (`aiplatform.googleapis.com`)
- Authenticated locally via:
  - `gcloud init`
  - `gcloud auth application-default login`

### Tech Stack
- Google ADK (`google-adk`)
- Vertex AI SDK (`google-cloud-aiplatform`)
- Optional: Google Cloud Storage (`google-cloud-storage`) for ingestion, `google-genai` if using Gemini SDK directly

### Setup
1) Use your existing Python environment (confirmed).
2) Install dependencies:

```bash
pip install -r /Users/shakirali/ai_code/aiAgent/rag_agent/requirements.txt
```

3) (Optional) Create a `.env` file for local configuration (project ID, region, model names). Example keys we may use later:

```bash
GCP_PROJECT_ID=
VERTEX_REGION=us-central1
GENERATION_MODEL=
EMBEDDING_MODEL=
GCS_BUCKET=
```

### Next Steps (Planned)
- Scaffold the ADK agent structure (no code committed yet)
- Implement corpus management tools (list/create/info/delete)
- Implement ingestion (GCS/Drive) and indexing with Vertex embeddings
- Implement query (retrieve → synthesize with model)
- Add a simple CLI or HTTP interface for testing

### References
- ADK documentation: `https://google.github.io/adk-docs/`
- ADK samples: `https://github.com/google/adk-samples`
- RAG agent sample: `https://github.com/bhancockio/adk-rag-agent/tree/main`

### Troubleshooting
- Re-run `pip install -r requirements.txt` after saving changes to dependencies
- Verify auth with `gcloud auth list` and `gcloud config list`
- Ensure the Vertex AI API is enabled and the correct project is selected


