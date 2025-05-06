# Streamlit Application for AI Resume Screening

This directory contains the Streamlit application for the AI Resume Screening platform. The Streamlit app is responsible for processing resumes, analyzing them against job descriptions, and generating summaries.

## Setup Instructions

1. **Install Dependencies**: Make sure you have Python installed. You can install the required packages using pip:

   ```
   pip install -r requirements.txt
   ```

2. **Environment Variables**: Create a `.env` file in this directory to store your environment variables. This should include your OpenAI API key and any other necessary configurations.

   Example `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Run the Streamlit App**: You can start the Streamlit application by running the following command in your terminal:

   ```
   streamlit run app.py
   ```

4. **Access the Application**: Once the app is running, you can access it in your web browser at `http://localhost:8501`.

## Features

- **Resume Upload**: Users can upload multiple PDF resumes for analysis.
- **Job Description Input**: Users can input a job description to match against the uploaded resumes.
- **Analysis and Summary**: The application analyzes the resumes and provides a match score along with a summary of each candidate's qualifications.

## File Structure

- `app.py`: The main Streamlit application file that handles user input and displays results.
- `utils.py`: Contains utility functions for processing resumes, extracting text, and generating summaries.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Your contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.