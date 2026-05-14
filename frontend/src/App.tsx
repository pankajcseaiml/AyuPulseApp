import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

// Pages
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { Dashboard } from './pages/Dashboard';
import { ProfilePage } from './pages/ProfilePage';
import { PatientsPage } from './pages/PatientsPage';
import { NewPredictionPage } from './pages/NewPredictionPage';
import { ResultsPage } from './pages/ResultsPage';
import { HistoryPage } from './pages/HistoryPage';
import { AdminPage } from './pages/AdminPage';

// Layout
import { DashboardLayout } from './components/layout/DashboardLayout';

function App() {
  const { user } = useAuth();

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <LoginPage />} />
      <Route path="/register" element={user ? <Navigate to="/dashboard" /> : <RegisterPage />} />

      {/* Protected routes */}
      <Route element={<DashboardLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/patients" element={<PatientsPage />} />
        
        {/* Predictions */}
        <Route path="/predictions/new" element={<NewPredictionPage />} />
        <Route path="/predictions/:id" element={<ResultsPage />} />
        <Route path="/history" element={<HistoryPage />} />
        
        {/* Admin only */}
        <Route 
          path="/admin" 
          element={(user?.role === 'admin' || user?.role === 'staff') ? <AdminPage /> : <Navigate to="/dashboard" />}
        />
      </Route>
      
      {/* Catch all */}
      <Route path="*" element={<Navigate to={user ? "/dashboard" : "/"} />} />
    </Routes>
  );
}

export default App;
