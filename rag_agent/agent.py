from google.adk.agents import Agent

from .tools.create_corpus import create_corpus
from .tools.list_corpora import list_corpora
from .tools.list_corpus_files import list_corpus_files
from .tools.add_data import add_data
from .tools.rag_query import rag_query
from .tools.delete_corpus import delete_corpus
from .prompts import root_agent_prompt

root_agent = Agent(
    name="rag_agent",
    model="gemini-2.5-flash-lite",
    description="RAG agent using vertex ai",
    tools=[
      create_corpus, 
      list_corpora,
      list_corpus_files,
      add_data,
      rag_query,
      delete_corpus,
    ],
    instruction=root_agent_prompt(),
)