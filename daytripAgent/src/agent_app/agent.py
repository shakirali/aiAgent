import os
import re
import asyncio
import google.generativeai as genai
import streamlit as st
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

def load_env() -> None:
    if load_dotenv is not None:
        load_dotenv()

def create_day_trip_agent(model: str) -> Agent:
    """Create the Spontaneous Day Trip Generator agent"""

    instruction="""
        You are the "Spontaneous Day Trip" Generator 🚗 - a specialized AI assistant that creates engaging full-day itineraries.

        Your Mission:
        Transform a simple mood or interest into a complete day-trip adventure with real-time details, while respecting a budget.

        Guidelines:
        1. **Budget-Aware**: Pay close attention to budget hints like 'cheap', 'affordable', or 'splurge'. Use Google Search to find activities (free museums, parks, paid attractions) that match the user's budget.
        2. **Full-Day Structure**: Create morning, afternoon, and evening activities.
        3. **Real-Time Focus**: Search for current operating hours and special events.
        4. **Mood Matching**: Align suggestions with the requested mood (adventurous, relaxing, artsy, etc.).

        RETURN itinerary in MARKDOWN FORMAT with clear time blocks and specific venue names.
        """

    agent = Agent(
        name="day_trip_agent",
        model=model,
        description="Agent specialized in generating spontaneous full-day itineraries based on mood, interests, and budget.",
        instruction=instruction,
        tools=[google_search],
    )
    return agent

async def run_agent(prompt: str) -> str:
    """Run the agent with the given prompt and return the response"""
    
    api_key = os.getenv("GOOGLE_API_KEY", "")
    model = os.getenv("MODEL", "gemini-2.5-flash")
    
    if not api_key:
        return "❌ Error: GOOGLE_API_KEY not set. Please set it in your .env file."
    
    day_trip_agent = create_day_trip_agent(model)
    session_service = InMemorySessionService()
    my_user_id = "adk_adventurer_001"

    runner = Runner(
        agent=day_trip_agent, 
        session_service=session_service,
        app_name=day_trip_agent.name
    )

    content = Content(
        parts=[Part(text=prompt)],
        role="user"
    )

    day_trip_session = await session_service.create_session(
        app_name=day_trip_agent.name,
        user_id=my_user_id
    )

    events = runner.run(
        user_id=my_user_id,
        session_id=day_trip_session.id,
        new_message=content
    )

    for event in events:
        if event.is_final_response():
            return event.content.parts[0].text
    
    return "No response generated."

def main():

    load_env()
    
    st.set_page_config(
        page_title="Day Trip Generator",
        page_icon="🚗",
        layout="wide"
    )
    
    st.title("🚗 Spontaneous Day Trip Generator")
    st.markdown("Create amazing day trip itineraries with AI!")

    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        model = st.selectbox(
            "Model",
            ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-pro"],
            index=0
        )
        
        # Check API key
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.error("❌ API Key not found")
            st.info("Set GOOGLE_API_KEY in your .env file")
    
    # Main input area
    user_prompt = st.text_area(
        "Describe your ideal day trip:",
        placeholder="e.g., Create a day trip itinerary to Milton Keynes, UK for me",
        height=100
    )
    
    # Generate button
    if st.button("🚀 Generate Day Trip", type="primary"):
        if not user_prompt.strip():
            st.warning("Please enter a prompt!")
        elif not api_key:
            st.error("API Key not configured!")
        else:
            with st.spinner("🧞 Generating your perfect day trip..."):
                try:
                    # Set the model in environment for this run
                    os.environ["MODEL"] = model
                    response = asyncio.run(run_agent(user_prompt))
                    st.markdown("## 🎉 Your Day Trip Itinerary")
                    st.markdown(response)
                except Exception as e:
                    st.error(f"❌ Error generating trip: {str(e)}")
    
    # Example prompts
    with st.expander("💡 Example prompts"):
        st.markdown("""
        - Create a day trip itinerary to Milton Keynes, UK for me
        - Plan a cheap day trip to London for art lovers
        - Generate an adventurous day trip to Edinburgh on a budget
        - Create a relaxing day trip to Bath with spa activities
        """)

if __name__ == "__main__":
    main()