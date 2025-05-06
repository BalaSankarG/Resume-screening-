import uuid
import numpy as np
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
import openrouter
import openai
import pdfplumber
import re
import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "balasankar560@gmail.com"
SENDER_PASSWORD = "wdsg rshh skpa oqln" 

# Set your OpenRouter API Key
openai.api_key = "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"  # Replace with your OpenRouter API key
openai.api_base = "https://openrouter.ai/api/v1"

# Extract text from PDF files
def get_pdf_text(pdf_doc):
    """
    Extract text content from a PDF file.
    """
    text = ""
    with pdfplumber.open(pdf_doc) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        print(text)
    return text
def extract_email_from_text(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    print (match)
    return match.group(0) if match else None

# Create Document objects from uploaded PDFs
def create_docs(user_pdf_list, unique_id):
    """
    Create Document objects from uploaded PDFs and their metadata.
    """
    docs = []
    for file in user_pdf_list:
        text = get_pdf_text(file)
        email = extract_email_from_text(text)

        # ✅ Print extracted email for verification
        print(f" Extracted Email from {file.name}: {email if email else 'No email found'}")
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
        print(docs)
    return docs

# Create embeddings for the job description and resumes
def create_embeddings_load_data():
    """
    Load the SentenceTransformer embeddings for the model "all-MiniLM-L6-v2".
    """
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Find similar resumes based on the job description
def find_similar_resumes(query, docs, embeddings, top_k=5):
    """
    Find the top K most similar resumes to the job description using cosine similarity.
    """
    query_embedding = np.array([embeddings.embed_query(query)]).astype('float32')
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
    You are an expert HR assistant.

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
        model="deepseek/deepseek-v3-base:free",
        messages=[
            {"role": "system", "content": "You are an expert HR assistant analyzing resume fit."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=700,
    )

    summary = response['choices'][0]['message']['content']
    return summary

def send_email_notification(to_email, score):
    subject = "Congratulations! You've Advanced to the Next Round"
    body = f"""Hi there,

Congratulations! Based on your resume screening score of {score}%, you've been shortlisted for the next round.

Our team will reach out to you with more details shortly.

Best regards,  
HR Team"""

    message = MIMEText(body)
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
