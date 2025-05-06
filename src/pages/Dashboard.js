import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ResumeUpload from '../components/ResumeUpload';
import Results from '../components/Results';
import './Dashboard.css';
const Dashboard = () => {
    const [jobPostings, setJobPostings] = useState([]);
    const [candidates, setCandidates] = useState([]);
    const [screeningReports, setScreeningReports] = useState([]);

    useEffect(() => {
        fetchJobPostings();
        fetchCandidates();
        fetchScreeningReports();
    }, []);

    const fetchJobPostings = async () => {
        try {
            const response = await axios.get('/api/job-postings'); // Adjust the endpoint as necessary
            setJobPostings(response.data);
        } catch (error) {
            console.error('Error fetching job postings:', error);
        }
    };

    const fetchCandidates = async () => {
        try {
            const response = await axios.get('/api/candidates'); // Adjust the endpoint as necessary
            setCandidates(response.data);
        } catch (error) {
            console.error('Error fetching candidates:', error);
        }
    };

    const fetchScreeningReports = async () => {
        try {
            const response = await axios.get('/api/screening-reports'); // Adjust the endpoint as necessary
            setScreeningReports(response.data);
        } catch (error) {
            console.error('Error fetching screening reports:', error);
        }
    };

    return (
        <div className="dashboard">
            <h1>HR Dashboard</h1>
            <ResumeUpload />
            <h2>Job Postings</h2>
            <ul>
                {jobPostings.map((job) => (
                    <li key={job.id}>{job.title}</li>
                ))}
            </ul>
            <h2>Candidates</h2>
            <ul>
                {candidates.map((candidate) => (
                    <li key={candidate.id}>{candidate.name}</li>
                ))}
            </ul>
            <h2>Screening Reports</h2>
            <Results reports={screeningReports} />
        </div>
    );
};

export default Dashboard;