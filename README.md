# aiAgent

Minimal scaffold for a Python agent using Google's Agent Development Kit (ADK).

References: see ADK docs at [Agent Development Kit](https://google.github.io/adk-docs/).

## Quick start

1. Create and activate a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Configure environment

```
cp env.sample .env
# edit .env and set GOOGLE_API_KEY and MODEL if desired
```

4. Run the Streamlit app

```
streamlit run src/agent_app/agent.py
```

The app will open in your browser at `http://localhost:8501`

## Project structure

```
.
├─ requirements.txt
├─ .gitignore
├─ env.sample
└─ src/
   └─ agent_app/
      ├─ __init__.py
      └─ agent.py          # Streamlit web interface
```

## Features

- 🚗 **Day Trip Generator**: AI-powered itinerary creation
- 🌐 **Web Interface**: User-friendly Streamlit UI
- 🔧 **Model Selection**: Choose between Gemini models
- 💰 **Budget Aware**: Respects budget constraints
- 🔍 **Real-time Search**: Uses Google Search for current info

## Notes

- This scaffold is intentionally minimal and uses ADK defaults. You can extend it with tools, workflows (Sequential/Parallel/Loop), or multi-agent setups as described in the ADK docs: [Agents](https://google.github.io/adk-docs/agents/).
- Ensure you have a valid `GOOGLE_API_KEY` configured. See ADK "Models & Authentication": [Docs](https://google.github.io/adk-docs/agents/models/).