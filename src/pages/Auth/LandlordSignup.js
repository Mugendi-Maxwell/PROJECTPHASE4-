import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signUpLandlord } from '../../api/api';
import './LandlordSignup.css';  // Import the CSS

function LandlordSignup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signUpLandlord(name, email, password);
      navigate('/landlord-dashboard/house-management');
    } catch (error) {
      console.error("Signup failed:", error);
    }
  };

  return (
    <div className="landlord-signup-container">
      <div className="landlord-signup-box">
        <h2>Landlord Signup</h2>
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

export default LandlordSignup;
