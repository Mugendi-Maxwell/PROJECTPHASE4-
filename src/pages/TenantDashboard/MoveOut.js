import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { moveOutTenant } from '../../api/api';
import './TenantMoveOut.css'; 


function TenantMoveOut() {
  const [tenantId, setTenantId] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleMoveOut = async (e) => {
    e.preventDefault();

    if (!tenantId.trim()) {
      setError('Please enter a valid Tenant ID.');
      return;
    }

    console.log("Submitting move-out request for tenant:", tenantId); // Debugging

    try {
      await moveOutTenant({ tenant_id: tenantId });
      navigate('/tenant-dashboard'); // Redirect after success
    } catch (err) {
      console.error("Move-out error:", err);
      setError("Failed to move out. Please try again.");
    }
  };

  return (
    <div>
      <h2>Move Out</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <p>Enter your Tenant ID and confirm to move out.</p>

      <form onSubmit={handleMoveOut}>
        <input
          type="text"
          placeholder="Enter Tenant ID"
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value)}
          required
        />
        <button type="submit">Confirm Move Out</button>
      </form>
    </div>
  );
}

export default TenantMoveOut;
