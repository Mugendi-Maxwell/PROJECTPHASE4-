import { useState } from 'react';
import { addHouse } from '../../api/api';
import './HouseManagement.css'; 

function HouseManagement() {
  const [address, setAddress] = useState('');
  const [apartmentCount, setApartmentCount] = useState('');
  const [rentPrice, setRentPrice] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addHouse({ address, apartmentCount, rentPrice });
      alert('House added successfully!');
    } catch (error) {
      console.error("Failed to add house:", error);
    }
  };

  return (
    <div className="house-management-container">
      <div className="house-management-box">
        <h2>Add House</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Address" 
            value={address} 
            onChange={(e) => setAddress(e.target.value)} 
          />
          <input 
            type="number" 
            placeholder="Number of Apartments" 
            value={apartmentCount} 
            onChange={(e) => setApartmentCount(e.target.value)} 
          />
          <input 
            type="number" 
            placeholder="Rent Price" 
            value={rentPrice} 
            onChange={(e) => setRentPrice(e.target.value)} 
          />
          <button type="submit">Add House</button>
        </form>
      </div>
    </div>
  );
}

export default HouseManagement;
