import uuid
import numpy as np
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
import pdfplumber
import re

# Extract text from PDF files
def get_pdf_text(pdf_doc):
    text = ""
    with pdfplumber.open(pdf_doc) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_email_from_text(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

# Create Document objects from uploaded PDFs
def create_docs(user_pdf_list, unique_id):
    docs = []
    for file in user_pdf_list:
        text = get_pdf_text(file)
        email = extract_email_from_text(text)

        docs.append(Document(
            page_content=text,
            metadata={
                "name": file.name,
                "id": uuid.uuid4().hex,
                "email": email,
                "type": file.type,
                "size": file.size,
                "unique_id": unique_id,
            }
        ))
    return docs

# Create embeddings for the job description and resumes
def create_embeddings_load_data():
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Generate a summary of the resume based on the job description
def get_summary(doc, job_description, score):
    prompt = f"""
    You are an expert HR assistant.

    Given the following job description:

    {job_description}

    And the following candidate resume:

    {doc.page_content}

    Your task is to analyze how well the resume matches the job description. Provide a structured summary with the following format:

    ### Resume Screening Report

    **Match Score (out of 100):**  
    {round(score * 100, 2)}

    **Key Matching Skills:**  
    - Skill 1  
    - Skill 2  
    - Skill 3  

    **Relevant Experience:**  
    - Experience 1  
    - Experience 2  

    **Missing Skills or Gaps:**  
    - Missing Skill 1  
    - Missing Skill 2  

    **Final Verdict:**  
    Strong Fit / Partial Fit / Not a Fit

    **Justification Summary:**  
    [Brief paragraph explaining the final verdict]
    """
    return prompt  # Placeholder for actual LLM call