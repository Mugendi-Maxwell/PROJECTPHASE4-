// src/api/api.js

const BASE_URL = 'http://localhost:8000';

// Login for Landlord
export const loginLandlord = async (email, password) => {
  const response = await fetch(`${BASE_URL}/login/landlord`, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Login failed');
  return response.json();
};

// Login for Tenant
export const loginTenant = async (email, password) => {
  const response = await fetch(`${BASE_URL}/login/tenant`, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Login failed');
  return response.json();
};

// Sign Up for Landlord
export const signUpLandlord = async (name, email, password) => {
  const response = await fetch(`${BASE_URL}/signup/landlord`, {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    console.error("Error response:", errorData);
    throw new Error(errorData.message || 'Signup failed');
  }
  return response.json();
};

// Sign Up for Tenant
export const signUpTenant = async (name, email, password) => {
  const response = await fetch(`${BASE_URL}/signup/tenant`, {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Signup failed');
  return response.json();
};


// Get the list of available houses
export const getHouseList = async () => {
  try {
    const response = await fetch(`${BASE_URL}/houses`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) {
      // Optionally, read the response text for more error info
      const errorText = await response.text();
      throw new Error(`Failed to fetch houses: ${errorText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error in getHouseList:", error);
    throw error;
  }
};


// Add a new house (for Landlord)
export const addHouse = async (houseData) => {
  const response = await fetch(`${BASE_URL}/houses`, {
    method: 'POST',
    body: JSON.stringify(houseData),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Failed to add house');
  return response.json();
};

// Move in a tenant (for Tenant)
export const moveInTenant = async (tenantData) => {
  const response = await fetch(`${BASE_URL}/tenants/move-in`, {
    method: 'POST',
    body: JSON.stringify(tenantData),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Move-in failed');
  return response.json();
};

// Move out a tenant (for Tenant)
export const moveOutTenant = async (tenantData) => {
  console.log("Sending tenant data:", tenantData);  // Debugging output

  const response = await fetch(`${BASE_URL}/tenants/move-out`, {
    method: 'POST',
    body: JSON.stringify(tenantData),
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Move-out failed:", errorText);  // Log backend response
    throw new Error('Move-out failed: ' + errorText);
  }

  return response.json();
};


// Make a rent payment (for Tenant)
export const payRent = async (paymentData) => {
  const response = await fetch(`${BASE_URL}/rent-payment`, {
    method: 'POST',
    body: JSON.stringify(paymentData),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Payment failed');
  return response.json();
};

// Submit a complaint (for Tenant)
export const submitComplaint = async (complaintData) => {
  const response = await fetch(`${BASE_URL}/complaints`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(complaintData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Failed to submit complaint');
  }

  return response.json();
};


// Update complaint status (for Landlord)
export const updateComplaintStatus = async (complaintId, status) => {
  const response = await fetch(`${BASE_URL}/complaints/status`, {
    method: 'POST',
    body: JSON.stringify({ complaint_id: complaintId, status }), // Use 'complaint_id' to match backend
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to update complaint status: ${errorText}`);
  }
  return response.json();
};


// Get Complaints for Landlord
export const getComplaints = async () => {
  const response = await fetch(`${BASE_URL}/complaints`);
  if (!response.ok) throw new Error('Failed to fetch complaints');
  return response.json();
};
