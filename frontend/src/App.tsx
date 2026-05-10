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
import NotificationToasts from '@/components/NotificationToasts';
import NotificationWatcher from '@/components/NotificationWatcher';

function ProtectedRoute({ element }: { element: React.ReactNode }) {
  const { user, authChecked } = useAuthStore();
  if (!authChecked) return null;
  return user ? element : <Navigate to="/login" />;
}

function PublicRoute({ element }: { element: React.ReactNode }) {
  const { user, authChecked } = useAuthStore();
  if (!authChecked) return null;
  return !user ? element : <Navigate to="/dashboard" />;
}

export default function App() {
  const { user, authChecked, initializeAuth } = useAuthStore();

  React.useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  if (!authChecked) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {user && <Navigation />}
        {user && <NotificationWatcher />}
        <NotificationToasts />
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
          <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
