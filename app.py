import streamlit as st
from pypdf import PdfReader
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
def highlight_keywords(text, keywords):
    keywords = sorted(set(keywords), key=lambda x: -len(x))  # Longest match first
    for word in keywords:
        pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
        text = pattern.sub(r'<mark style="background-color: #fff3cd;"><b>\1</b></mark>', text)
    return text


# Streamlit page setup
st.set_page_config(page_title="Research Paper Analyzer", layout="wide")

# Custom CSS to match your Figma style
st.markdown("""
    <style>
    html, body {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
    }
    .title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        color: #5c5c5c;
        margin-bottom: 30px;
    }
    .panel {
        background-color: #f6f8fa;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .button-row button {
        background-color: #0074D9;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Main title & subtitle
st.markdown("<div class='title'>📄 Research Paper Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Understand, summarize, and critique your research paper with AI assistance.</div>", unsafe_allow_html=True)

# 2-column layout: controls (left), output (right)
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("### 📂 Upload & Options")
    uploaded_file = st.file_uploader("Upload your research paper (PDF)", type=["pdf"])
    
    st.markdown("#### 🛠️ Customization")
    review_type = st.radio("Select Review Type", ["Summary", "Critique", "Highlights & Weaknesses"])
    tone = st.selectbox("Select Tone", ["Formal", "Conversational", "Technical", "Simplified"])
    audience = st.selectbox("Target Audience", ["Expert", "Layperson", "Student", "Professional"])

    run_analysis = st.button("🔍 Analyze", type ="primary", use_container_width=True)

with right:
    if uploaded_file and run_analysis:  
        # Extract text from PDF
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

        if len(text) > 15000:
            st.warning("Text is too long. Trimming to first 15,000 characters.")
            text = text[:15000]

        # Generate prompt
        prompt = f"""You are an academic research assistant with expertise in analyzing research papers. You have a phd in the field of artifical intelligence and have read thousands of research papers. 
The user has uploaded a research paper. Provide a {review_type.lower()} in a {tone.lower()} tone, 
intended for a {audience.lower()} audience.
sUse headings like:
- Abstract Summary
- Research Objective
- Methodology Insights
- Strengths & Limitations
- Conclusion"""
        if tone == "Technical":
            prompt += " Use technical jargon and detailed explanations."
        elif tone == "Simplified":
            prompt += " Use simple language and avoid jargon."
        elif tone == "Conversational":
            prompt += " Use a friendly and engaging tone, as if explaining to a friend."
        elif tone == "Formal":
            prompt += " Use a formal and academic tone, suitable for scholarly communication."


        prompt =+ """Research paper content: 
                \"\"\"
                    {text}
                \"\"\"
        """

        # --- Ask GPT to extract important keywords (scientific, technical, conceptual) ---
        with st.spinner("Extracting keywords..."):
             keyword_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI that extracts important keywords and technical terms from research papers."},
                    {"role": "user", "content": f"List the 10–15 most important keywords or technical terms from the following paper. Just return a comma-separated list.\n\n{text}"}
                ]
            )
        keyword_text = keyword_response.choices[0].message.content
        keywords = [kw.strip().lower() for kw in keyword_text.split(",")]


        with st.spinner("Analyzing the paper with GPT..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant trained to analyze research papers."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content

        highlighted_output = highlight_keywords(result, keywords)

        st.markdown("### 🧠 GPT Review with Highlighted Keywords")
        st.markdown(highlighted_output, unsafe_allow_html=True)

        st.markdown("### 🔑 Extracted Keywords")
        st.markdown(f"<div style='background-color:#f8f9fa;padding:10px;border-radius:8px;'>"
            f"{', '.join(keywords)}</div>", unsafe_allow_html=True)

    elif not uploaded_file:
        st.info("Please upload a PDF to get started.")

