"""
AI Services Module.
Handles all interactions with the Google Gemini API, including chat sessions,
function calling (tools), and multimodal inputs.
"""

import os
from typing import Optional, List, Dict, Any, Union
import google.generativeai as genai
from google.generativeai.types import content_types
from PIL import Image

import streamlit as st
from config import Config
from utils.logger import setup_logger
from google_workspace import add_election_reminder_to_calendar, find_polling_location_via_maps

logger = setup_logger(__name__)

# Configure API
if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=Config.GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
You are Civic Nexus, an expert, impartial, and highly accessible Election Intelligence Agent. 
Your goal is to educate users on the election process, timelines, and necessary steps to vote.

Key Guidelines:
1. **Impartiality:** Never show bias towards any political party, candidate, or ideology.
2. **Clarity & Accessibility:** Explain complex processes in simple language (target reading level: 8th grade). Use markdown lists for steps.
3. **Accuracy:** Provide factual information.
4. **Tools:** Use available tools to look up specific state data when asked.
5. **Multimodality:** If the user uploads an image (e.g., of a sample ballot), explain what it is and guide them on how to fill it out or understand it.
"""

# Dummy data for the tool
STATE_DEADLINES = {
    "california": "Online: Oct 21, By Mail: Postmarked by Oct 21, In-Person: Nov 5",
    "texas": "In-Person/Mail: Oct 7",
    "new york": "Online/Mail/In-Person: Oct 26",
    "florida": "Online/Mail/In-Person: Oct 7"
}

@st.cache_data
def get_state_registration_deadline(state_name: str) -> str:
    """
    Looks up the voter registration deadline for a given US state.
    
    Args:
        state_name: The full name of the US state (e.g., 'California', 'Texas').
        
    Returns:
        A string containing the registration deadline(s) for that state.
    """
    logger.info(f"Tool called: get_state_registration_deadline for state={state_name}")
    state_key = state_name.lower().strip()
    return STATE_DEADLINES.get(state_key, f"I don't have the specific deadline data for {state_name} on hand. Please check your local state election website.")


class ElectionAssistant:
    """
    Manages the chat session with Gemini, preserving conversation history
    and handling multimodal inputs and tool calls.
    """
    def __init__(self) -> None:
        """Initializes the Gemini model and starts a chat session."""
        logger.info("Initializing ElectionAssistant")
        try:
            # We use gemini-1.5-pro-latest which supports multimodality and tools
            self.model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                tools=[get_state_registration_deadline, add_election_reminder_to_calendar, find_polling_location_via_maps],
                system_instruction=SYSTEM_INSTRUCTION
            )
            # Start chat session with empty history
            self.chat_session = self.model.start_chat(enable_automatic_function_calling=True)
            logger.info("Chat session started successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            self.model = None
            self.chat_session = None

    def send_message(self, message: str, image: Optional[Image.Image] = None) -> str:
        """
        Sends a message (and optional image) to the Gemini model and returns the response.
        
        Args:
            message (str): The user's text prompt.
            image (Optional[Image.Image]): An optional PIL Image object (e.g., a sample ballot).
            
        Returns:
            str: The assistant's text response.
        """
        if not self.chat_session:
            logger.error("Chat session is not initialized.")
            return "Error: Assistant is not properly initialized. Please check API key."

        try:
            logger.info(f"Sending message to Gemini. Image included: {image is not None}")
            
            # Construct content payload
            content: List[Any] = [message]
            if image:
                content.append(image)
                
            response = self.chat_session.send_message(content)
            logger.info("Received response from Gemini.")
            return response.text
            
        except Exception as e:
            logger.error(f"Error during send_message: {e}", exc_info=True)
            return f"An error occurred while processing your request: {str(e)}"
