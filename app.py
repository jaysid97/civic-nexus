"""
Main Streamlit Application UI for Election Process Education.
"""

import streamlit as st
from PIL import Image
from services import ElectionAssistant
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Civic Nexus: Election Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_assistant() -> ElectionAssistant:
    """Cached initialization of the ElectionAssistant."""
    logger.info("Initializing new ElectionAssistant via cache.")
    return ElectionAssistant()

if "assistant" not in st.session_state:
    st.session_state.assistant = get_assistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar UI ---
with st.sidebar:
    st.title("🏛️ Civic Nexus")
    st.markdown("Your interactive guide to understanding the election process. Accessible, impartial, and accurate.")
    
    st.divider()
    
    st.subheader("🛠️ Features")
    st.markdown("- **Multimodal Analysis:** Upload an image of a ballot to get help understanding it.")
    st.markdown("- **State Lookup:** Ask for deadlines in states like California, Texas, Florida, or New York.")
    
    st.divider()
    
    st.subheader("📎 Document Upload")
    uploaded_file = st.file_uploader("Upload a sample ballot or voter ID image", type=["png", "jpg", "jpeg"])
    
    st.divider()
    
    # Quick action buttons
    st.subheader("⚡ Quick Actions")
    if st.button("How do I register to vote?", use_container_width=True):
        st.session_state.quick_prompt = "How do I register to vote? Please provide a step-by-step guide."
    if st.button("What is the deadline in California?", use_container_width=True):
        st.session_state.quick_prompt = "What is the voter registration deadline in California?"


# --- Main UI ---
st.title("Civic Nexus: Election Intelligence")
st.markdown("""
Welcome to **Civic Nexus**. I am an enterprise-grade AI agent designed to help you navigate the election process. 
You can ask me questions, use the quick actions in the sidebar, or even upload an image of an election-related document for me to analyze.
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Determine prompt from user input or quick action button
prompt = st.chat_input("Ask a question about the election process...")

if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    # 1. Display user message
    st.chat_message("user").markdown(prompt)
    
    # Process image if uploaded
    img = None
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            st.toast("Image loaded successfully!", icon="✅")
        except Exception as e:
            st.error(f"Failed to load image: {e}")
            logger.error(f"Image load error: {e}")

    # Add to history
    msg_content = prompt
    if img:
         msg_content += "\n*(Image uploaded with this prompt)*"
    st.session_state.messages.append({"role": "user", "content": msg_content})

    # 2. Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing request..."):
            try:
                response = st.session_state.assistant.send_message(message=prompt, image=img)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                logger.error(f"Generation error: {e}", exc_info=True)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
