import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginLandlord } from '../../api/api';
import './LandlordLogin.css';  // Import the CSS

function LandlordLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await loginLandlord(email, password);
      
      // Store landlordId in a cookie
      document.cookie = `landlordId=${response.landlordId}; path=/; max-age=${60 * 60 * 24 * 7}`;

      navigate('/landlord-dashboard');
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <div className="landlord-login-container">
      <div className="landlord-login-box">
        <h2>Landlord Login</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="email" 
            placeholder="Email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required
          />
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default LandlordLogin;
