
import os
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to extract text from a PDF file
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to generate a summary using the Gemini API
def get_gemini_summary(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Summarize the following text:\n\n{text}")
    return response.text

# Function to generate a quiz using the Gemini API
def get_gemini_quiz(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Create a quiz from the following text:\n\n{text}")
    return response.text

def main():
    st.set_page_config(page_title="Study Notes Summarizer and Quiz Generator", page_icon=":books:")
    st.header("Study Notes Summarizer and Quiz Generator")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Summarizer", "Quiz Generator"])

    if page == "Summarizer":
        st.subheader("Summarize your study notes")
        pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True)

        if st.button("Summarize"):
            if pdf_docs:
                with st.spinner("Summarizing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    summary = get_gemini_summary(raw_text)
                    st.success("Summary Generated!")
                    st.write(summary)
            else:
                st.warning("Please upload at least one PDF file.")

    elif page == "Quiz Generator":
        st.subheader("Generate a quiz from your study notes")
        pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True)

        if st.button("Create Quiz"):
            if pdf_docs:
                with st.spinner("Creating quiz..."):
                    raw_text = get_pdf_text(pdf_docs)
                    quiz = get_gemini_quiz(raw_text)
                    st.success("Quiz Created!")
                    st.write(quiz)
            else:
                st.warning("Please upload at least one PDF file.")

if __name__ == "__main__":
    main()
