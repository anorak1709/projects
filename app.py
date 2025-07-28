import os
import openai
import gradio as gr
from openai import OpenAI
from redlines import Redlines
from pypdf import PdfReader
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#Initialize OpenAI client
client = OpenAI(api_key=openai.api_key)

#Extract text from the uploaded PDF file
def extract_pdf_text(file):
    reader = PdfReader(file.name) 
    complete_text = ""
    for page in reader.pages:
        complete_text += page.extract_text() + "\n"
    return complete_text.strip()

# Make grammatical changes and change the tone of the text using OpenAI's API
def get_openai_response(text, tone=None):
    system_prompt = "You are a professional editor and writing assistant. Correct grammar, spelling, punctuation, and clarity. Show the improved version."
    system_prompt += "You have the qualifications of a professional editor who has completed a PhD in English and has 20 years of experience in editing and writing."

#To get better output we give the model a much better prompt that helps is think in a more structured way
    if tone:
        system_prompt += f" Rewrite the text in a {tone} tone."
    elif tone == "Gen-z":
        system_prompt += " Rewrite the text in a Gen-Z tone, using slang and informal language. Make it sound trendy and relatable to a younger audience."
    elif tone == "Kafkaesque":
        system_prompt += " Rewrite the text in a Kafkaesque tone, making it surreal, nightmarish, and absurd. Use complex and disorienting language to create a sense of unease."
        system_prompt += "Franz Kafka's profound sadness stemmed from a confluence of personal struggles, including a difficult relationship with his father, health issues, and feelings of alienation and self-doubt."
    
    response = client.chat.completions.create(
        model="gpt-4o mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

#Unified handler that accepts both PDF and text input
def grammar_corrector(text=None, file=None, tone=""):
    if file:
        text = extract_pdf_text(file)

    if not text:
        return "", "", "{}"

    corrected = get_openai_response(text, tone)
    json_output = {
        "original text": text,
        "corrected text": corrected
    }

    return text, corrected, json_output

#Gradio
iface = gr.Interface(
    fn=grammar_corrector,
    inputs=[
        gr.Textbox(label="Enter the text you want to edit", lines=10, placeholder="Or upload a PDF below"),
        gr.File(label="Upload PDF", file_types=[".pdf"]),
        gr.Dropdown(label="Tone", choices=["", "Formal", "Assertive", "Negative", "Sarcastic", "Humorous", "Kafkaesque", "Gen-z"], value="")
    ],
    outputs=[
        gr.Textbox(label="Original Text", lines=10),
        gr.Textbox(label="Corrected Text", lines=10),
        gr.JSON(label="JSON Output")
    ],
    title="Grammar Checker",
    description="Correct grammar. Upload PDF or type text. Get side-by-side corrections"
)

if __name__ == "__main__":
    iface.launch()
