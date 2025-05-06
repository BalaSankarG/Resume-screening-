import uuid
import numpy as np
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
import openrouter
import openai
import pdfplumber
import re
import smtplib
from email.mime.text import MIMEText
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("Loading embeddings model at startup...")
EMBEDDINGS_MODEL = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
print("Embeddings model loaded.")

SENDER_EMAIL = "balasankar560@gmail.com"
SENDER_PASSWORD = "wdsg rshh skpa oqln" 

# Set your OpenRouter API Key
openai.api_key = "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"  # Replace with your OpenRouter API key
openai.api_base = "https://openrouter.ai/api/v1"

# Extract text from PDF files
def extract_email_from_text(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

import warnings

def get_pdf_text(pdf_path):
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    print(text)
    return text

def create_docs(user_pdf_list, unique_id):
    docs = []
    for file in user_pdf_list:
        
        text = get_pdf_text(file["resume_path"])  # Use the file path
        email = extract_email_from_text(text)
        docs.append(Document(
            page_content=text,
            metadata={
                "name": file["name"],
                "id": unique_id,
                "email": email,
            }
        ))
    print(email)
    print(docs)
    return docs

# Create embeddings for the job description and resumes
def create_embeddings_load_data():
    return EMBEDDINGS_MODEL

# Find similar resumes based on the job description
def find_similar_resumes(query, docs, embeddings, top_k=5):
    """
    Find the top K most similar resumes to the job description using cosine similarity.
    """
    query_embedding = np.array([embeddings.embed_query(query)]).astype('float32').reshape(1, -1)
    resume_embeddings = [embeddings.embed_query(doc.page_content) for doc in docs]

    # Calculate cosine similarity between the job description and each resume
    scores = cosine_similarity(query_embedding, resume_embeddings)[0]

    # Rank resumes based on similarity score
    ranked_resumes = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return ranked_resumes[:top_k]

# Generate a summary of the resume based on the job description
def get_summary(doc, job_description, score, current_doc):
    """
    Generate a structured summary of the resume using an OpenRouter-hosted LLM.
    This summary helps HR quickly evaluate a candidate against the job description
    
    """
    prompt = f"""
    You are an expert HR assistant. so give me a structured format of the following and it will in the short form and acore the candidate based on the below content of job description and the pagecontent i given 

    Given the following job description:

    {job_description}

    And the following candidate resume:

    {doc.page_content}

    Your task is to analyze how well the resume matches the job description. Provide a structured summary with the following format:

    ### Resume Screening Report

    **Match Score (out of 100):**  
    [Give a number based on how well the candidate matches the job description with score  ]
    the score is
   { round(score * 100, 2)}

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

    response = openai.ChatCompletion.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You are an expert HR assistant analyzing resume fit."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=1024,
    )

    summary = response['choices'][0]['message']['content']
    return summary

def send_email_notification(to_email, score):
    subject = "Update on Your Job Application"
    body = f"""Hii,

Thank you for applying to our company. Based on your resume screening score of {score}%, we are pleased to inform you that you have been shortlisted for the next round of our recruitment process.

Our HR team will contact you soon with further details.

Best regards,
HR Team
{SENDER_EMAIL}
"""

    message = MIMEText(body)
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        print(f"✅ Email sent to {to_email}")
        return "Sent"
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return "Failed"