import React from 'react';
import './JobCard.css';

const JobCard = ({ job, onApply }) => (
  <div className="job-card">
    <h3>{job.title}</h3>
    <p>{job.description}</p>
    {onApply && (
      <button className="apply-btn" onClick={() => onApply(job.id)}>
        Apply
      </button>
    )}
  </div>
);

export default JobCard;