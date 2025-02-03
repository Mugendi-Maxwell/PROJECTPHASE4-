import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHouseList, moveInTenant } from '../../api/api';
import './MoveIn.css';


function MoveIn() {
  const [houses, setHouses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [maxRent, setMaxRent] = useState('');
  const [tenantId, setTenantId] = useState('');
  const [houseId, setHouseId] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHouses = async () => {
      try {
        // Call getHouseList and extract houses array from the response.
        const data = await getHouseList();
        const housesArray = data.houses || data; // If API returns { houses: [...] }
        setHouses(housesArray);
      } catch (error) {
        console.error("Failed to fetch houses:", error);
      }
    };

    fetchHouses();
  }, []);

  // Filter houses by search term (search by address or rent price)
  const filteredHouses = houses.filter(house => {
    const matchesAddress = house.address.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRentPrice = maxRent ? house.rent_price <= parseFloat(maxRent) : true;
    return matchesAddress && matchesRentPrice;
  });

  const handleMoveIn = async () => {
    try {
      // Ensure both tenantId and houseId are provided
      if (!tenantId || !houseId) {
        alert('Please provide both Tenant ID and House ID.');
        return;
      }

      // Call the API to update the tenant's house (move in)
      await moveInTenant({ tenant_id: tenantId, house_id: houseId });
      
      // Redirect to Rent Payment page with the selected houseId and tenantId as query params
      navigate(`/tenant-dashboard/rent-payment?houseId=${houseId}&tenantId=${tenantId}`);
    } catch (error) {
      console.error("Failed to move in:", error);
    }
  };

  return (
    <div>
      <h2>Available Houses</h2>
      
      <div>
        <input
          type="text"
          placeholder="Search by address..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <input
          type="number"
          placeholder="Max Rent Price"
          value={maxRent}
          onChange={(e) => setMaxRent(e.target.value)}
        />
      </div>

      <div>
        <input
          type="text"
          placeholder="Tenant ID"
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value)}
        />
        <input
          type="text"
          placeholder="House ID"
          value={houseId}
          onChange={(e) => setHouseId(e.target.value)}
        />
      </div>

      <ul>
        {filteredHouses.map((house) => (
          <li key={house.id}>
            {house.address} - Rent: {house.rent_price} - Vacant: {house.vacant_apartments} 
            <br />
            <strong>House ID:</strong> {house.id} 
            <button onClick={() => setHouseId(house.id)}>Select House</button>
          </li>
        ))}
      </ul>

      <button onClick={handleMoveIn}>Move In</button>
    </div>
  );
}

export default MoveIn;
