# AI Resume Screening Platform - Frontend

## Overview
This project is a full-stack AI resume screening platform that utilizes a React frontend, FastAPI backend, and MongoDB for data storage. The platform allows users to upload resumes, analyze them against job descriptions, and view results, including match scores and summaries.

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm (Node package manager)
- Access to the FastAPI backend and MongoDB database

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-resume-screening-platform/frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```

### Running the Application
To start the React application, run:
```
npm start
```
This will start the development server and open the application in your default web browser.

### Folder Structure
- **public/**: Contains static files like `index.html`.
- **src/**: Contains the source code for the React application.
  - **components/**: Reusable components such as `ResumeUpload` and `Results`.
  - **pages/**: Different pages of the application, including `Home` and `Dashboard`.
  - **styles/**: CSS files for styling the application.

### API Integration
The frontend communicates with the FastAPI backend to handle resume uploads and retrieve analysis results. Ensure the backend is running and accessible at the specified endpoint.

### Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.