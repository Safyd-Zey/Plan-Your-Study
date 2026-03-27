import '@/index.css';
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store';

// Pages
import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import DashboardPage from '@/pages/DashboardPage';
import CoursesPage from '@/pages/CoursesPage';
import AssignmentsPage from '@/pages/AssignmentsPage';
import SchedulePage from '@/pages/SchedulePage';
import ProgressPage from '@/pages/ProgressPage';

// Components
import Navigation from '@/components/Navigation';

function ProtectedRoute({ element }: { element: React.ReactNode }) {
  const { token } = useAuthStore();
  return token ? element : <Navigate to="/login" />;
}

function PublicRoute({ element }: { element: React.ReactNode }) {
  const { token } = useAuthStore();
  return !token ? element : <Navigate to="/dashboard" />;
}

export default function App() {
  const { token } = useAuthStore();

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {token && <Navigation />}
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<PublicRoute element={<LoginPage />} />} />
          <Route path="/register" element={<PublicRoute element={<RegisterPage />} />} />

          {/* Protected Routes */}
          <Route path="/dashboard" element={<ProtectedRoute element={<DashboardPage />} />} />
          <Route path="/courses" element={<ProtectedRoute element={<CoursesPage />} />} />
          <Route path="/assignments" element={<ProtectedRoute element={<AssignmentsPage />} />} />
          <Route path="/schedule" element={<ProtectedRoute element={<SchedulePage />} />} />
          <Route path="/progress" element={<ProtectedRoute element={<ProgressPage />} />} />

          {/* Fallback */}
          <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
