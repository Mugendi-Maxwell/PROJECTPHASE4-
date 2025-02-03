import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  getComplaints, 
  getLandlordTenantStatus, 
  updateComplaintStatus, 
  moveInTenant, 
  addHouse 
} from '../../api/api';
import './LandlordDashboard.css'
const BASE_URL = 'http://localhost:8000';

function LandlordDashboard() {
  const [landlordId, setLandlordId] = useState('');
  const [houses, setHouses] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [rentStatus, setRentStatus] = useState([]);
  const [tenants, setTenants] = useState([]);
  const [newHouse, setNewHouse] = useState({
    address: '',
    num_apartments: '',
    rent_price: '',
  });
  const [selectedHouseId, setSelectedHouseId] = useState(null);

  const navigate = useNavigate();

  // Fetch houses for the landlord when landlordId changes
  useEffect(() => {
    if (!landlordId) return;

    const fetchHousesData = async () => {
      try {
        const response = await fetch(`${BASE_URL}/houses?landlord_id=${landlordId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to fetch houses: ${errorText}`);
        }
        const data = await response.json();
        // Handle two possibilities:
        // 1. Data is directly an array.
        // 2. Data is an object with a property "houses" that is an array.
        const housesArray = Array.isArray(data)
          ? data
          : (Array.isArray(data.houses) ? data.houses : []);
        setHouses(housesArray);
      } catch (error) {
        console.error("Failed to fetch houses:", error);
        setHouses([]); // Default to empty array on error
      }
    };

    fetchHousesData();
  }, [landlordId]);

  // Fetch complaints for the landlord
  useEffect(() => {
    if (!landlordId) return;

    const fetchComplaintsData = async () => {
      try {
        const response = await fetch(`${BASE_URL}/complaints?landlord_id=${landlordId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch complaints");
        }
        const data = await response.json();
        // Assuming response returns { complaints: [...] } or directly an array
        const complaintsArray = Array.isArray(data)
          ? data
          : (Array.isArray(data.complaints) ? data.complaints : []);
        setComplaints(complaintsArray);
      } catch (error) {
        console.error("Error fetching complaints:", error);
      }
    };

    fetchComplaintsData();
  }, [landlordId]);

  // Fetch rent status for the landlord
  useEffect(() => {
    if (!landlordId) return;

    const fetchRentStatusData = async () => {
      try {
        const response = await fetch(`${BASE_URL}/rent-status?landlord_id=${landlordId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch rent status");
        }
        const data = await response.json();
        const rentStatusArray = Array.isArray(data)
          ? data
          : (Array.isArray(data.rentStatus) ? data.rentStatus : []);
        setRentStatus(rentStatusArray);
      } catch (error) {
        console.error("Error fetching rent status:", error);
      }
    };

    fetchRentStatusData();
  }, [landlordId]);

  // Local helper function to fetch tenants for a specific house
  const fetchTenantsForHouse = async (houseId) => {
    try {
      const response = await fetch(`${BASE_URL}/tenants?house_id=${houseId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch tenants: ${errorText}`);
      }
      const data = await response.json();
      const allTenants = Array.isArray(data)
        ? data
        : (Array.isArray(data.tenants) ? data.tenants : []);
      const filteredTenants = allTenants.filter(tenant => tenant.house_id === Number(houseId));
      setTenants(filteredTenants);
    } catch (error) {
      console.error("Error fetching tenants:", error);
      setTenants([]);
    }
  };

  // When a house is selected, fetch its tenants and its complaints (filtered by house)
  useEffect(() => {
    if (!selectedHouseId) {
      setTenants([]);
      return;
    }
    const fetchHouseDetails = async () => {
      try {
        await fetchTenantsForHouse(selectedHouseId);
        // Fetch complaints for the selected house
        const response = await fetch(`${BASE_URL}/complaints?house_id=${selectedHouseId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to fetch complaints for house: ${errorText}`);
        }
        const data = await response.json();
        const complaintsArray = Array.isArray(data)
          ? data
          : (Array.isArray(data.complaints) ? data.complaints : []);
        setComplaints(complaintsArray);
      } catch (error) {
        console.error("Failed to fetch house details:", error);
      }
    };

    fetchHouseDetails();
  }, [selectedHouseId]);

  // Handle adding a new house
  const handleAddHouse = async (e) => {
    e.preventDefault();
    if (!landlordId) {
      console.error("Landlord ID is required.");
      return;
    }
    const houseWithLandlordId = {
      ...newHouse,
      landlord_id: Number(landlordId),
    };

    try {
      const response = await fetch(`${BASE_URL}/houses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(houseWithLandlordId),
      });

      if (!response.ok) {
        throw new Error("Failed to add house");
      }

      // Refresh house list after adding a new house
      const updatedResponse = await fetch(`${BASE_URL}/houses?landlord_id=${landlordId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const updatedData = await updatedResponse.json();
      const updatedHouses = Array.isArray(updatedData)
        ? updatedData
        : (Array.isArray(updatedData.houses) ? updatedData.houses : []);
      setHouses(updatedHouses);
      setNewHouse({ address: '', num_apartments: '', rent_price: '' });
    } catch (error) {
      console.error("Failed to add house:", error);
    }
  };

  // Handler for updating a complaint's status (e.g., marking as resolved)
  const handleComplaintStatusUpdate = async (complaintId, newStatus) => {
    try {
      await updateComplaintStatus(complaintId, newStatus);
      // Refresh complaints for the selected house
      const response = await fetch(`${BASE_URL}/complaints?house_id=${selectedHouseId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch complaints: ${errorText}`);
      }
      const data = await response.json();
      const updatedComplaints = Array.isArray(data)
        ? data
        : (Array.isArray(data.complaints) ? data.complaints : []);
      setComplaints(updatedComplaints);
    } catch (error) {
      console.error("Failed to update complaint status:", error);
    }
  };

  return (
    <div>
      <h2>Landlord Dashboard</h2>

      {/* Landlord ID Input */}
      <div>
        <label>Enter Your Landlord ID:</label>
        <input
          type="number"
          value={landlordId}
          onChange={(e) => setLandlordId(e.target.value)}
        />
      </div>

      {/* Form to Add House */}
      <form onSubmit={handleAddHouse}>
        <input
          type="text"
          placeholder="Address"
          value={newHouse.address}
          onChange={(e) => setNewHouse({ ...newHouse, address: e.target.value })}
        />
        <input
          type="number"
          placeholder="Number of Apartments"
          value={newHouse.num_apartments}
          onChange={(e) => setNewHouse({ ...newHouse, num_apartments: e.target.value })}
        />
        <input
          type="number"
          placeholder="Rent Price"
          value={newHouse.rent_price}
          onChange={(e) => setNewHouse({ ...newHouse, rent_price: e.target.value })}
        />
        <button type="submit">Add House</button>
      </form>

      {/* Display Houses */}
      <h3>Houses for Landlord {landlordId}</h3>
      <ul>
        {houses.map((house) => (
          <li key={house.id}>
            {house.address} - {house.num_apartments} apartments - Rent: {house.rent_price} - Vacant: {house.vacant_apartments}
            <br />
            <strong>House ID:</strong> {house.id}
            <button onClick={() => setSelectedHouseId(house.id)}>View Details</button>
          </li>
        ))}
      </ul>

      {/* Selected House Details */}
      {selectedHouseId && (
        <div>
          <h3>Details for House ID: {selectedHouseId}</h3>

          {/* Tenants Section */}
          <h4>Tenants</h4>
          <ul>
            {tenants.length > 0 ? (
              tenants.map((tenant) => (
                <li key={tenant.id}>
                  {tenant.name} (ID: {tenant.id})
                </li>
              ))
            ) : (
              <li>No tenants found for this house.</li>
            )}
          </ul>

          {/* Rent Status Section */}
          <h4>Rent Status</h4>
          <ul>
            {rentStatus.length > 0 ? (
              rentStatus.map((status) => (
                <li key={status.tenantId}>
                  Tenant {status.tenantName}: {status.rentPaid ? 'Paid' : 'Unpaid'}
                </li>
              ))
            ) : (
              <li>No rent status data available for this house.</li>
            )}
          </ul>

          {/* Complaints Section */}
          <h4>Complaints</h4>
          <ul>
            {complaints.length > 0 ? (
              complaints.map((complaint) => (
                <li key={complaint.id}>
                  {complaint.description} - Status: {complaint.status}
                  {complaint.status === "Pending" && (
                    <button onClick={() => handleComplaintStatusUpdate(complaint.id, "Resolved")}>
                      Mark as Resolved
                    </button>
                  )}
                </li>
              ))
            ) : (
              <li>No complaints found for this house.</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export default LandlordDashboard;
