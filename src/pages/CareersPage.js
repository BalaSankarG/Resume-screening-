import React, { useState, useEffect } from 'react';
import JobCard from '../components/JobCard';
import './CareersPage.css';
const CareersPage = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [candidateName, setCandidateName] = useState('');
  const [resumeFile, setResumeFile] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/jobs')
      .then((response) => response.json())
      .then((data) => setJobs(data));
  }, []);

  const handleApply = (jobId) => {
    if (!resumeFile) {
      alert('Please upload your resume file.');
      return;
    }
    const formData = new FormData();
    formData.append('name', candidateName);
    formData.append('resume', resumeFile);

    fetch(`http://localhost:5000/api/jobs/${jobId}/apply`, {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        setCandidateName('');
        setResumeFile(null);
        setSelectedJob(null);
      });
  };
  return (
    <div>
      <h2>Careers</h2>
      <div className="job-list">
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            onApply={() => setSelectedJob(job)}
          />
        ))}
      </div>
      {selectedJob && (
  <div className="apply-popup">
    <h3>Apply for {selectedJob.title}</h3>
    <input
      type="text"
      placeholder="Your Name"
      value={candidateName}
      onChange={(e) => setCandidateName(e.target.value)}
    />
    <input
      type="file"
      accept=".pdf,.doc,.docx"
      onChange={(e) => setResumeFile(e.target.files[0])}
    />
    <button onClick={() => handleApply(selectedJob.id)}>Submit Application</button>
  </div>
)}
    </div>
  );
};

export default CareersPage;