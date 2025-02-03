// src/pages/HomePage.js
import { Link } from 'react-router-dom';
import './HomePage.css'; // Import the CSS file for styling

function HomePage() {
  return (
    <div className="home-container">
      <div className="home-content">
        <h1>Welcome to the House Management System</h1>
        <p>Your one-stop solution for renting houses, managing payments, and posting complaints.</p>
        <div className="home-buttons">
          <Link to="/landlord-login" className="home-btn landlord-btn">Landlord Login</Link>
          <Link to="/tenant-login" className="home-btn tenant-btn">Tenant Login</Link>
          <Link to="/landlord-signup" className="home-btn landlord-signup-btn">Landlord Signup</Link>
          <Link to="/tenant-signup" className="home-btn tenant-signup-btn">Tenant Signup</Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
