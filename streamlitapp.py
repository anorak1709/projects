import streamlit as st
import time

# NOTE: The original `run_therapy_workflow` is assumed to be available.
# For demonstration purposes, we will mock its behavior.
def run_therapy_workflow(user_input):
    """
    Simulates the AI therapist's response.
    In a real app, this would call the CrewAI workflow.
    """
    time.sleep(1) # Simulate thinking time
    if "hello" in user_input.lower() or "hi" in user_input.lower():
        return "Hello there. Thank you for reaching out. What's on your mind today?"
    elif "sad" in user_input.lower():
        return "I hear you. It sounds like you're going through a tough time. Can you tell me a little more about what's making you feel sad?"
    elif "anxious" in user_input.lower():
        return "Anxiety can be a heavy feeling. Let's explore that together. What are some of the things you've been feeling anxious about recently?"
    else:
        return "Thank you for sharing that. I'm here to listen. Please continue whenever you feel ready."

# --- CUSTOM CSS FOR ANIMATIONS AND STYLING ---
# This CSS makes the app look more modern and adds simple animations.
# We use st.markdown with unsafe_allow_html=True to inject the CSS.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* General body styling */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f6;
    }

    /* Container for the whole app */
    .stApp {
        background-color: ##FF0000;
    }
    
    /* Main title animation */
    .animated-title {
        text-align: center;
        color: #4CAF50  ;
        font-size: 3em;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 40px;
        animation: fadeInDown 1s ease-in-out;
    }
    .animated-title span {
        font-size: 0.8em;
        font-weight: 300;
        color: #555;
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-in-out;
    }
    .stChatMessage.user {
        background-color: #e0f7fa;
        color: #00796b;
        margin-left: 20%;
    }
    .stChatMessage.assistant {
        background-color: #fff;
        color: #333;
        margin-right: 20%;
    }
    
    /* Chat input styling */
    .stChatInput {
        background-color: #fff;
        padding: 10px;
        border-radius: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Tabs styling */
    .stTabs [data-testid="stTabContent"] {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTabs [data-testid="stTabList"] button {
        font-size: 1.1em;
        font-weight: 700;
        color: #555;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.2em;
        font-weight: 700;
        color: #388e3c;
    }

    /* Fade-in animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)


# --- SET UP STREAMLIT PAGE ---
st.set_page_config(
    page_title="Zenith AI Therapist",
    page_icon="�",
    layout="wide",  # Use a wide layout for a better user experience
    initial_sidebar_state="expanded"
)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://placehold.co/150x150/4CAF50/FFFFFF?text=Zenith+AI", use_column_width=True)
    st.header("Zenith AI Therapist")
    st.markdown("Your mental health companion 💬. We're here to listen and support you in a safe, confidential space.")
    
    st.divider()

    st.info("⚠️ This app is not a replacement for professional help. If you're in crisis, please contact a mental health hotline or a trusted professional. Your well-being is our top priority.")

# --- MAIN PAGE CONTENT ---
st.markdown("<div class='animated-title'>Welcome to Zenith <span>AI Therapist</span></div>", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []  # Each message is a dict: {"role": "user"/"assistant", "content": "..."}

# --- TABS FOR ORGANIZED UI ---
tab1, tab2, tab3 = st.tabs(["💬 Chat", "✨ Insights", "🔗 Resources"])

# --- TAB 1: CHAT INTERFACE ---
with tab1:
    st.subheader("How are you feeling today?")
    st.markdown("Feel free to share what's on your mind. I'm here to help you explore your thoughts and feelings.")

    # Display all past messages
    # The custom CSS will handle the styling and animation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input box
    if user_input := st.chat_input("Type something you're feeling or thinking..."):
        # Display user message in chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get response from AI (using the mocked function)
        with st.spinner("Therapist is responding..."):
            response = run_therapy_workflow(user_input)

        # Display AI message
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- TAB 2: INSIGHTS ---
with tab2:
    st.subheader("Summary & Insights")
    st.markdown("This section provides a high-level overview of your conversations. As you talk more, this will grow more helpful.")
    
    if st.session_state.messages:
        with st.expander("Your Conversation History", expanded=True):
            for i, msg in enumerate(st.session_state.messages):
                st.markdown(f"**{msg['role'].capitalize()} {i+1}:** {msg['content']}")
        
        st.divider()

        # Mocking an insight component. In a real app, this would be generated by the AI.
        st.metric(label="Total Interactions", value=len(st.session_state.messages))
        
        with st.expander("Potential Themes & Keywords"):
            st.markdown("Based on our last few conversations, some potential themes are:")
            st.markdown("- **Emotions:** Sadness, Anxiety")
            st.markdown("- **Triggers:** Work-related stress, Social situations")
            st.markdown("*(Note: This is a simulated insight based on keywords.)*")
    else:
        st.info("Start a conversation in the 'Chat' tab to see insights here.")

# --- TAB 3: RESOURCES ---
with tab3:
    st.subheader("Support & Resources")
    st.markdown("Here are some helpful links and information that you might find useful.")

    with st.expander("Mental Health Hotlines"):
        st.markdown("""
        If you are in immediate danger or a crisis, please seek professional help.
        - **National Suicide Prevention Lifeline:** 988
        - **Crisis Text Line:** Text HOME to 741741
        - **SAMHSA's National Helpline:** 1-800-662-HELP (4357)
        """)

    with st.expander("Recommended Reading"):
        st.markdown("""
        - [Mindfulness for Beginners](https://example.com/mindfulness)
        - [Coping with Anxiety](https://example.com/anxiety)
        - [The Power of Positive Thinking](https://example.com/positive-thinking)
        """)
        
    with st.expander("Breathing Exercise"):
        st.markdown("Try this simple breathing exercise to calm your mind.")
        st.image("https://placehold.co/600x200/cccccc/333333?text=Breathing+Exercise+GIF", use_column_width=True)

