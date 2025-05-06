+-------------------+         +-------------------+         +-------------------+
|                   |         |                   |         |                   |
|   HR Dashboard    |<------->|    Backend API    |<------->|   Applications    |
| (Job Posting,     |         | (Flask:           |         |  (jobs.json,      |
|  Analyze, Delete) |         |  Resume Screening |         |   applications.json|
|                   |         |  & Management)    |         |                   |
+-------------------+         +-------------------+         +-------------------+
         ^                           ^   ^                           ^
         |                           |   |                           |
         |                           |   |                           |
         |                           |   |                           |
+-------------------+         +-------------------+         +-------------------+
|                   |         |                   |         |                   |
|   Candidate UI    |-------> |   AI/NLP Module   |<------->|   Email Service   |
| (Apply, Upload    |         | (Embeddings,      |         | (SMTP, Gmail)     |
|  Resume)          |         |  Similarity, LLM) |         |                   |
|                   |         |                   |         |                   |
+-------------------+         +-------------------+         +-------------------+