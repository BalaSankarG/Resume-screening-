from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from utils import create_docs, create_embeddings_load_data, find_similar_resumes, get_summary, send_email_notification

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

JOBS_FILE = "jobs.json"
APPLICATIONS_FILE = "applications.json"

def load_jobs():
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, "r") as f:
            return json.load(f)
    return []

def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f)

def load_applications():
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_applications(applications):
    with open(APPLICATIONS_FILE, "w") as f:
        json.dump(applications, f)

@app.route('/api/jobs', methods=['POST'])
def post_job():
    jobs = load_jobs()
    applications = load_applications()
    data = request.json
    job_title = data.get('title')
    job_description = data.get('description')
    if not job_title or not job_description:
        return jsonify({"error": "Missing required fields"}), 400
    job = {
        "id": len(jobs) + 1,
        "title": job_title,
        "description": job_description
    }
    jobs.append(job)
    applications[str(job["id"])] = []
    save_jobs(jobs)
    save_applications(applications)
    return jsonify({"message": "Job posted successfully", "job": job})

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = load_jobs()
    return jsonify(jobs)

@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def apply_for_job(job_id):
    jobs = load_jobs()
    applications = load_applications()
    if job_id > len(jobs) or job_id <= 0:
        return jsonify({"error": "Invalid job ID"}), 404

    name = request.form.get('name')
    resume_file = request.files.get('resume')
    if not name or not resume_file:
        return jsonify({"error": "Missing required fields"}), 400

    filename = f"{name}_{resume_file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(filepath)

    applications[str(job_id)].append({
        "name": name,
        "resume_path": filepath
    })
    save_applications(applications)
    return jsonify({"message": "Application submitted successfully"})

@app.route('/api/jobs/<int:job_id>/applications', methods=['GET'])
def get_applications(job_id):
    jobs = load_jobs()
    applications = load_applications()
    if job_id > len(jobs) or job_id <= 0:
        return jsonify({"error": "Invalid job ID"}), 404
    return jsonify(applications.get(str(job_id), []))

@app.route('/api/jobs/<int:job_id>/analyze', methods=['POST'])
def analyze_applications(job_id):
    try:
        jobs = load_jobs()
        applications = load_applications()
        print("Starting analysis for job", job_id)
        if job_id > len(jobs) or job_id <= 0:
            print("Invalid job ID")
            return jsonify({"error": "Invalid job ID"}), 404
        data = request.json
        job_description = data.get('job_description')
        if not job_description:
            print("Missing job description")
            return jsonify({"error": "Missing job description"}), 400
        resumes = applications.get(str(job_id), [])
        print("Loaded resumes:", resumes)
        unique_id = "default_unique_id"
        try:
            docs = create_docs(resumes, unique_id)
            print("Created docs")
        except Exception as e:
            print("Error creating docs:", e)
            return jsonify({"error": "Failed to create docs"}), 500
        try:
            embeddings = create_embeddings_load_data()
            print("Loaded embeddings")
        except Exception as e:
            print("Error loading embeddings:", e)
            return jsonify({"error": "Failed to load embeddings"}), 500
        try:
            relevant_docs = find_similar_resumes(job_description, docs, embeddings, top_k=len(resumes))
            print("Found similar resumes")
            with open("similarity_scores.txt", "w") as f:
                for doc, score in relevant_docs:
                    f.write(str(score) + "\n")
        except Exception as e:
            print("Error finding similar resumes:", e)
            return jsonify({"error": "Failed to find similar resumes"}), 500
        results = []
        for doc, score in relevant_docs:
            print("Processing doc:", doc.metadata["name"])
            try:
                summary = get_summary(doc, job_description, score, doc)
            except Exception as e:
                print("Error generating summary:", e)
                summary = "Summary generation failed."
            email_status = "Not Sent"
            if score > 0.50 and doc.metadata.get("email"):
                try:
                    email_status = send_email_notification(doc.metadata["email"], round(score * 100, 2))
                except Exception as e:
                    print(f"Error sending email to {doc.metadata.get('email')}: {e}")
                    email_status = "Failed to send"
            results.append({
                "candidate_name": doc.metadata["name"],
                "match_score": round(score * 100, 2),
                "email_status": email_status,
                "summary": summary
            })
        print("Returning results")
        return jsonify({"results": results})
    except Exception as e:
        print("Error in /analyze:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == "hr" and password == "123":
        return jsonify({"message": "Login successful", "role": "HR"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/api/jobs/<int:job_id>/applications', methods=['DELETE'])
def delete_applications(job_id):
    jobs = load_jobs()
    applications = load_applications()
    if str(job_id) in applications:
        applications[str(job_id)] = []
        save_applications(applications)
        return jsonify({"message": f"All applications for job {job_id} deleted."}), 200
    else:
        return jsonify({"error": "No applications found for this job."}), 404

if __name__ == '__main__':
    app.run(debug=True)