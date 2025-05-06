import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './HRDashboard.css';
const HRDashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [applications, setApplications] = useState([]);
  const [results, setResults] = useState([]);
  const [jobForm, setJobForm] = useState({ title: '', description: '' });
  const navigate = useNavigate();

  useEffect(() => {
    const isAuthenticated = localStorage.getItem('auth') === 'true';
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [navigate]);

  useEffect(() => {
    fetch('http://localhost:5000/api/jobs')
      .then((response) => response.json())
      .then((data) => setJobs(data));
  }, []);

  const handleViewApplications = (job) => {
    setSelectedJob(job);
    fetch(`http://localhost:5000/api/jobs/${job.id}/applications`)
      .then((response) => response.json())
      .then((data) => setApplications(data));
    setResults([]);
  };

  const handleAnalyze = () => {
    fetch(`http://localhost:5000/api/jobs/${selectedJob.id}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_description: selectedJob.description }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setResults(data.results))
      .catch((error) => {
        console.error('Error during analyze fetch:', error);
        alert('Failed to fetch analysis results. Please check the backend server and try again.');
      });
  };

  const handlePostJob = () => {
    fetch('http://localhost:5000/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(jobForm),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        setJobs([...jobs, data.job]);
        setJobForm({ title: '', description: '' });
      });
  };

  return (
    <div>
      <h2>HR Dashboard</h2>
      <div>
        <h3>Post a New Job</h3>
        <input
          type="text"
          placeholder="Job Title"
          value={jobForm.title}
          onChange={(e) => setJobForm({ ...jobForm, title: e.target.value })}
        />
        <textarea
          placeholder="Job Description"
          value={jobForm.description}
          onChange={(e) => setJobForm({ ...jobForm, description: e.target.value })}
        />
        <button onClick={handlePostJob}>Post Job</button>
      </div>
      <h3>Posted Jobs</h3>
      <ul>
        {jobs.map((job) => (
          <li key={job.id}>
            <h4>{job.title}</h4>
            <p>{job.description}</p>
            <button onClick={() => handleViewApplications(job)}>View Applications</button>
          </li>
        ))}
      </ul>
      {selectedJob && (
        <div>
          <h3>Applications for {selectedJob.title}</h3>
          <button onClick={handleAnalyze}>Analyze Applications</button>
          <ul>
            {applications.map((app, idx) => (
              <li key={idx}>
                <strong>{app.name}</strong>: {app.resume}
              </li>
            ))}
          </ul>
        </div>
      )}
      {results.length > 0 && (
        <table border="1">
          <thead>
            <tr>
              <th>Candidate Name</th>
              <th>Match Score</th>
              <th>Email Status</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, idx) => (
              <tr key={idx}>
                <td>{result.candidate_name}</td>
                <td>{result.match_score}%</td>
                <td>{result.email_status}</td>
                <td>
                  <details>
                    <summary>View Summary</summary>
                    <pre>{result.summary}</pre>
                  </details>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default HRDashboard;
