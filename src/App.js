import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import Navbar from './components/Navbar';
import CareersPage from './pages/CareersPage';
import HRDashboard from './pages/HRDashboard';
import LoginPage from './pages/LoginPage';
import ProtectedRoute from './components/ProtectedRoute';
const App = () => (
<Router>
<Navbar />
<Routes>
  <Route path="/" element={<HomePage />} />
  <Route path="/careers" element={<CareersPage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route
    path="/hr"
    element={
      <ProtectedRoute>
        <HRDashboard />
      </ProtectedRoute>
    }
  />
</Routes>
</Router>
);

export default App;