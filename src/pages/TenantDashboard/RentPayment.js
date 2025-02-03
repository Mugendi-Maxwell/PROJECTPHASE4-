import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { payRent } from '../../api/api';

function TenantPayRent() {
  const [tenantId, setTenantId] = useState('');
  const [amount, setAmount] = useState('');
  const navigate = useNavigate();

  const handlePayment = async (e) => {
    e.preventDefault();

    if (!tenantId.trim() || !amount || amount <= 0) {
      alert('Please enter a valid Tenant ID and rent amount.');
      return;
    }

    try {
      await payRent({ tenant_id: tenantId, amount });

      navigate('/tenant-dashboard'); // Redirect after successful payment
    } catch (error) {
      console.error("Payment failed:", error);
      alert("Payment failed. Please try again.");
    }
  };

  return (
    <div>
      <h2>Pay Rent</h2>
      <form onSubmit={handlePayment}>
        <input
          type="text"
          placeholder="Enter Tenant ID"
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Enter Rent Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
          min="1"
        />
        <button type="submit">Pay Rent</button>
      </form>
    </div>
  );
}

export default TenantPayRent;
