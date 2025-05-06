import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

with open("similarity_scores.txt") as f:
    similarity_scores = [float(line.strip()) for line in f]

plt.hist(similarity_scores, bins=10, color='skyblue', edgecolor='black')
plt.title('Distribution of Resume Similarity Scores')
plt.xlabel('Cosine Similarity Score')
plt.ylabel('Number of Resumes')
plt.show()

plt.figure(figsize=(4,4))
plt.boxplot(similarity_scores, vert=True, patch_artist=True)
plt.title('Boxplot of Similarity Scores')
plt.ylabel('Cosine Similarity Score')
plt.show()

# 3. Violin plot
plt.figure(figsize=(4,4))
plt.violinplot(similarity_scores, vert=True)
plt.title('Violin Plot of Similarity Scores')
plt.ylabel('Cosine Similarity Score')
plt.show()

# 4. Pie chart for score ranges
ranges = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
labels = ['0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0']
counts = [len([s for s in similarity_scores if ranges[i] < s <= ranges[i+1]]) for i in range(len(ranges)-1)]
plt.figure(figsize=(5,5))
plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Score Range Distribution')
plt.show()

similarity_matrix = np.random.rand(5, 10)  # 5 jobs, 10 resumes

plt.figure(figsize=(8, 5))
plt.imshow(similarity_matrix, cmap='viridis', aspect='auto')
plt.colorbar(label='Cosine Similarity Score')
plt.xlabel('Resume Index')
plt.ylabel('Job Index')
plt.title('Heatmap of Resume Similarity Scores (Jobs vs. Resumes)')
plt.show()


y_true = [1, 0, 1, 0, 1]  # Actual labels
y_pred = [1 if s > 0.5 else 0 for s in similarity_scores]  # Predicted by threshold

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.show()

print("Total resumes:", len(similarity_scores))
print("Min score:", min(similarity_scores))
print("Max score:", max(similarity_scores))
print("Mean score:", np.mean(similarity_scores))
print("Median score:", np.median(similarity_scores))
print("Std deviation:", np.std(similarity_scores))