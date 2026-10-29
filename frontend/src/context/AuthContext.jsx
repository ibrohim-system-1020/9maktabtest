import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user_info');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handleLogout = () => setUser(null);
    window.addEventListener('auth_logout', handleLogout);

    const token = localStorage.getItem('access_token');
    if (token) {
      api.getMe()
        .then((userData) => {
          setUser(userData);
          localStorage.setItem('user_info', JSON.stringify(userData));
        })
        .catch(() => {
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }

    return () => window.removeEventListener('auth_logout', handleLogout);
  }, []);

  const login = async (username, password) => {
    const res = await api.login(username, password);
    setUser(res.user);
    return res.user;
  };

  const register = async (registrationData) => {
    const res = await api.register(registrationData);
    setUser(res.user);
    return res.user;
  };

  const logout = () => {
    api.logout();
    setUser(null);
  };

  const isRole = (...roles) => {
    if (!user) return false;
    return roles.includes(user.role);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        role: user?.role || null,
        loading,
        login,
        register,
        logout,
        isRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
