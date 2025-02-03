import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitComplaint } from '../../api/api';
import './TenantComplaints.css'; 


function TenantComplaints() {
  const [tenantId, setTenantId] = useState('');
  const [complaint, setComplaint] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleComplaintSubmit = async (e) => {
    e.preventDefault();

    if (!tenantId.trim() || !complaint.trim()) {
      setError('Please enter a valid Tenant ID and Complaint.');
      return;
    }

    try {
      await submitComplaint({ tenant_id: tenantId, complaint });
      alert('Complaint submitted successfully.');
      navigate('/tenant-dashboard'); // Redirect after submission
    } catch (err) {
      console.error('Complaint submission failed:', err);
      setError('Failed to submit complaint. Please try again.');
    }
  };

  return (
    <div>
      <h2>Submit a Complaint</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      <form onSubmit={handleComplaintSubmit}>
        <input
          type="text"
          placeholder="Enter Tenant ID"
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value)}
          required
        />
        <textarea
          placeholder="Enter your complaint"
          value={complaint}
          onChange={(e) => setComplaint(e.target.value)}
          required
        />
        <button type="submit">Submit Complaint</button>
      </form>
    </div>
  );
}

export default TenantComplaints;
