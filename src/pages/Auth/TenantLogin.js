import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginTenant } from '../../api/api';
import './TenantLogin.css'; // Import the CSS

function TenantLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await loginTenant(email, password);
      console.log("Login response:", response);
      
      if (response && response.token) {
        localStorage.setItem('token', response.token);
        navigate('/tenant-dashboard');
      } else {
        console.error("Login failed: Invalid response structure", response);
      }
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <div className="tenant-login-container">
      <div className="tenant-login-box">
        <h2>Tenant Login</h2>
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

export default TenantLogin;
