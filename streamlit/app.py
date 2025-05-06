import streamlit as st
from dotenv import load_dotenv
from utils import *
import uuid
import requests

if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] = ''

def main():
    load_dotenv()
    st.set_page_config(page_title="Resume Screening Assistance")
    st.markdown('<style>p {font-size: 20px;}</style>', unsafe_allow_html=True)
    st.title("AI Resume Screening")

    job_description = st.text_area("Job Description", key="1")
    document_count = st.text_input("Number of Resumes to Return", key="2")

    pdf = st.file_uploader("Upload resumes (PDF only)", type=["pdf"], accept_multiple_files=True)

    submit = st.button("🚀 Analyze Resumes")

    if submit:
        if not job_description or not document_count or not pdf:
            st.warning("Please fill in the job description, number of resumes, and upload at least one file.")
            return

        with st.spinner('Analyzing resumes...'):
            st.session_state['unique_id'] = uuid.uuid4().hex

            # STEP 1: Extract resume data
            final_docs_list = create_docs(pdf, st.session_state['unique_id'])
            st.write(f"Resumes Uploaded: {len(final_docs_list)}")

            # STEP 2: Load embeddings
            embeddings = create_embeddings_load_data()

            # STEP 3: Match with job description
            relevant_docs = find_similar_resumes(job_description, final_docs_list, embeddings, int(document_count))

            st.write(":heavy_minus_sign:" * 30)

            # STEP 4: Display results and notify
            for i, (doc, score) in enumerate(relevant_docs):
                st.subheader(f"Resume {i + 1}")
                st.write(f"**File Name:** {doc.metadata['name']}")

                candidate_email = doc.metadata.get("email", "Not found")
                match_score = round(score * 100, 2)
                st.info(f"**Match Score:** {match_score}%")

                # Send email if score > 60
                email_status = ""
                if score > 0.60 and candidate_email and candidate_email != "Not found":
                    email_status = send_email_notification(candidate_email, match_score)
                elif not candidate_email or candidate_email == "Not found":
                    email_status = "Email not found in resume. Cannot notify."
                else:
                    email_status = "Score below threshold. No email sent."

                st.write(f"Email Notification Status: {email_status}")

                with st.expander("Show Screening Summary"):
                    summary = get_summary(doc, job_description, score, current_doc=None)
                    st.write(summary)

# Run the app
if __name__ == '__main__':
    main()