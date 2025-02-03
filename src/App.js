// src/App.js
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandlordLogin from './pages/Auth/LandlordLogin';
import TenantLogin from './pages/Auth/TenantLogin';
import LandlordSignup from './pages/Auth/LandlordSignup';
import TenantSignup from './pages/Auth/TenantSignup';
import LandlordDashboard from './pages/LandlordDashboard/LandlordDashboard';
import HouseManagement from './pages/LandlordDashboard/HouseManagement';
import TenantDashboard from './pages/TenantDashboard/TenantDashboard';
import MoveIn from './pages/TenantDashboard/MoveIn';
import MoveOut from './pages/TenantDashboard/MoveOut';
import RentPayment from './pages/TenantDashboard/RentPayment';
import Complaints from './pages/TenantDashboard/Complaints';
import HomePage from './pages/HomePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} /> {/* Home Page Route */}
        <Route path="/landlord-login" element={<LandlordLogin />} />
        <Route path="/tenant-login" element={<TenantLogin />} />
        <Route path="/landlord-signup" element={<LandlordSignup />} />
        <Route path="/tenant-signup" element={<TenantSignup />} />
        
        {/* Landlord Dashboard Routes */}
        <Route path="/landlord-dashboard" element={<LandlordDashboard />} />
        <Route path="/landlord-dashboard/house-management" element={<HouseManagement />} />
        
        {/* Tenant Dashboard Routes */}
        <Route path="/tenant-dashboard" element={<TenantDashboard />} />
        <Route path="/tenant-dashboard/move-in" element={<MoveIn />} />
        <Route path="/tenant-dashboard/move-out" element={<MoveOut />} />
        <Route path="/tenant-dashboard/rent-payment" element={<RentPayment />} />
        <Route path="/tenant-dashboard/complaints" element={<Complaints />} />
        
      </Routes>
    </Router>
  );
}

export default App;
