// src/pages/TenantDashboard/TenantDashboard.js
import React from 'react';
import { Link } from 'react-router-dom';
import './TenantDashboard.css';

function TenantDashboard() {
  return (
    <div>
      <h2>Tenant Dashboard</h2>
      <nav>
        <ul>
          <li>
            <Link to="/tenant-dashboard/move-in">Move In</Link>
          </li>
          <li>
            <Link to="/tenant-dashboard/move-out">Move Out</Link>
          </li>
          <li>
            <Link to="/tenant-dashboard/rent-payment">Rent Payment</Link>
          </li>
          <li>
            <Link to="/tenant-dashboard/complaints">Submit Complaint</Link>
          </li>
        </ul>
      </nav>
      {/* Additional dashboard content can be added here */}
    </div>
  );
}

export default TenantDashboard;
