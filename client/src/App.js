import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ConversationProvider } from './contexts/ConversationContext';
import './index.css';

function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/chat" /> : <LoginPage />} />
      <Route path="/chat" element={user ? <ChatPage /> : <Navigate to="/login" />} />
      <Route path="/profile" element={user ? <ProfilePage /> : <Navigate to="/login" />} />
      <Route path="/" element={<Navigate to={user ? "/chat" : "/login"} />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <ConversationProvider>
        <Router>
          <div className="App">
            <AppRoutes />
          </div>
        </Router>
      </ConversationProvider>
    </AuthProvider>
  );
}

export default App;
