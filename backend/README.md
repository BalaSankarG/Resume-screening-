# AI Resume Screening Platform Backend

This document provides instructions for setting up and running the backend service of the AI Resume Screening Platform.

## Prerequisites

- Python 3.7 or higher
- MongoDB (local or cloud instance)
- pip (Python package installer)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ai-resume-screening-platform/backend
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up MongoDB:**
   - Ensure your MongoDB server is running.
   - Update the connection string in `backend/app/utils/database.py` if necessary.

2. **Environment Variables:**
   - You may need to set environment variables for sensitive information such as database credentials and API keys. Create a `.env` file in the `backend` directory and add your variables there.

## Running the Application

1. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be accessible at `http://127.0.0.1:8000`.

2. **API Documentation:**
   - You can access the automatically generated API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

- **User Authentication:**
  - `POST /users/register`: Register a new user.
  - `POST /users/login`: Log in an existing user.

- **Resume Processing:**
  - `POST /resumes/upload`: Upload resumes for analysis.
  - `GET /resumes/results`: Retrieve analysis results.

## Testing

To run tests, ensure you have the necessary testing libraries installed and execute:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- FastAPI for the web framework.
- MongoDB for the database.
- Streamlit for resume processing.