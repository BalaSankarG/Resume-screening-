from app import load_applications, create_docs
from langchain_community.embeddings import SentenceTransformerEmbeddings
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
)

# Set your job description here (fetch from your jobs.json or type directly)
job_description = "We are looking for a passionate and driven AI & Data Science Engineer to join our team. As a fresh graduate with hands-on experience in machine learning, NLP, and web development, you’ll help build intelligent applications, conduct data analysis, and collaborate on cutting-edge projects involving AI tools and frameworks. ..."

# Load resumes for a specific job_id
job_id = 1  # Change as needed
applications = load_applications()
resumes = applications.get(str(job_id), [])
docs = create_docs(resumes, unique_id="compare_models")
resume_texts = [doc.page_content for doc in docs]
resume_names = [doc.metadata["name"] for doc in docs]

# Load both models
model1 = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
model2 = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Get embeddings for job description
jd_emb1 = model1.embed_query(job_description)
jd_emb2 = model2.embed_query(job_description)

# Get embeddings for resumes
res_embs1 = [model1.embed_query(resume) for resume in resume_texts]
res_embs2 = [model2.embed_query(resume) for resume in resume_texts]

# Cosine similarity function
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Calculate similarity scores
scores_model1 = [cosine_similarity(jd_emb1, emb) for emb in res_embs1]
scores_model2 = [cosine_similarity(jd_emb2, emb) for emb in res_embs2]

# Print comparison table
print(f"{'Resume':<20} {'Model 1':<10} {'Model 2':<10}")
for name, s1, s2 in zip(resume_names, scores_model1, scores_model2):
    print(f"{name:<20} {s1:<10.2f} {s2:<10.2f}")

# Plot bar chart
x = np.arange(len(resume_names))
width = 0.35

plt.bar(x - width/2, scores_model1, width, label='Model 1 (mpnet)')
plt.bar(x + width/2, scores_model2, width, label='Model 2 (MiniLM)')
plt.xlabel('Resume')
plt.ylabel('Similarity Score')
plt.title('Model Comparison: Resume Similarity Scores')
plt.xticks(x, resume_names, rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('model_comparison.png')
plt.show()

# --------- Evaluation with labels ---------
# Example: 1 = good fit, 0 = not fit (set according to your HR review)
labels = [1, 0, 1, 0, 1,0,1]  # <-- Replace with your actual labels, length must match resume_names

if len(labels) == len(resume_names):
    pred1 = [1 if s > 0.5 else 0 for s in scores_model1]
    pred2 = [1 if s > 0.5 else 0 for s in scores_model2]

    # Model 1 metrics
    acc1 = accuracy_score(labels, pred1)
    prec1 = precision_score(labels, pred1, zero_division=0)
    rec1 = recall_score(labels, pred1, zero_division=0)
    f1_1 = f1_score(labels, pred1, zero_division=0)
    auc1 = roc_auc_score(labels, scores_model1)
    cm1 = confusion_matrix(labels, pred1)

    # Model 2 metrics
    acc2 = accuracy_score(labels, pred2)
    prec2 = precision_score(labels, pred2, zero_division=0)
    rec2 = recall_score(labels, pred2, zero_division=0)
    f1_2 = f1_score(labels, pred2, zero_division=0)
    auc2 = roc_auc_score(labels, scores_model2)
    cm2 = confusion_matrix(labels, pred2)

    print("\nModel 1 (mpnet):")
    print(f"Accuracy:  {acc1:.2f}")
    print(f"Precision: {prec1:.2f}")
    print(f"Recall:    {rec1:.2f}")
    print(f"F1 Score:  {f1_1:.2f}")
    print(f"ROC-AUC:   {auc1:.2f}")
    print("Confusion Matrix:\n", cm1)

    print("\nModel 2 (MiniLM):")
    print(f"Accuracy:  {acc2:.2f}")
    print(f"Precision: {prec2:.2f}")
    print(f"Recall:    {rec2:.2f}")
    print(f"F1 Score:  {f1_2:.2f}")
    print(f"ROC-AUC:   {auc2:.2f}")
    print("Confusion Matrix:\n", cm2)

    # Plot confusion matrices
    disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1)
    disp1.plot(cmap='Blues')
    plt.title('Confusion Matrix - Model 1 (mpnet)')
    plt.show()

    disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2)
    disp2.plot(cmap='Greens')
    plt.title('Confusion Matrix - Model 2 (MiniLM)')
    plt.show()
else:
    print("\nLabel count does not match number of resumes. Evaluation skipped.")