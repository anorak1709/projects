import streamlit as st
from workflows.therapy_workflow import run_therapy_workflow

# Set up Streamlit page
st.set_page_config(page_title="AI Therapist", page_icon="🧠", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.title("🧠 AI Therapist")
    st.markdown("Your mental health companion 💬")
    st.info("⚠️ This app is not a replacement for professional help.\n\nIf you're in crisis, please contact a mental health hotline.")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []  # Each message is a dict: {"role": "user"/"assistant", "content": "..."}

# --- Chat Display ---
st.title("💬 How are you feeling today?")

# Display all past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input box ---
if user_input := st.chat_input("Type something you're feeling or thinking..."):
    # Display user message in chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from CrewAI
    with st.spinner("Therapist is responding..."):
        response = run_therapy_workflow(user_input)

    # Display AI message
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
