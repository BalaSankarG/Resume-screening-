import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => (
  <nav style={{ padding: '1rem', background: '#eee', marginBottom: '2rem' }}>
    <Link to="/" style={{ marginRight: '1rem' }}>Home</Link>
    <Link to="/careers" style={{ marginRight: '1rem' }}>Careers</Link>
    
    <Link to="/login">HR Login</Link>
  </nav>
);
export default Navbar;