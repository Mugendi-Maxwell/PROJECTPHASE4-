import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signUpTenant } from '../../api/api';
import './TenantSignup.css'; // Import the CSS

function TenantSignup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signUpTenant(name, email, password);
      navigate('/tenant-login');
    } catch (error) {
      console.error("Signup failed:", error);
    }
  };

  return (
    <div className="tenant-signup-container">
      <div className="tenant-signup-box">
        <h2>Tenant Signup</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Name" 
            value={name} 
            onChange={(e) => setName(e.target.value)}
            required
          />
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
          <button type="submit">Sign Up</button>
        </form>
      </div>
    </div>
  );
}

export default TenantSignup;
