import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

// Access-токен хранится только в памяти (не в localStorage/sessionStorage)
let _accessToken = null;

export function getAccessToken() {
  return _accessToken;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Пытаемся восстановить сессию через refresh-cookie при загрузке
  useEffect(() => {
    const restore = async () => {
      try {
        const res = await api.post('/api/auth/token/refresh/');
        _accessToken = res.data.access;
        const meRes = await api.get('/api/auth/me/', {
          headers: { Authorization: `Bearer ${_accessToken}` },
        });
        setUser(meRes.data);
      } catch {
        _accessToken = null;
      } finally {
        setLoading(false);
      }
    };
    restore();
  }, []);

  // Настраиваем interceptors один раз
  useEffect(() => {
    const reqId = api.interceptors.request.use((config) => {
      if (_accessToken) {
        config.headers.Authorization = `Bearer ${_accessToken}`;
      }
      return config;
    });

    const resId = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const original = error.config;
        if (error.response?.status === 401 && !original._retry) {
          original._retry = true;
          try {
            const res = await api.post('/api/auth/token/refresh/');
            _accessToken = res.data.access;
            original.headers.Authorization = `Bearer ${_accessToken}`;
            return api(original);
          } catch {
            _accessToken = null;
            setUser(null);
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.request.eject(reqId);
      api.interceptors.response.eject(resId);
    };
  }, []);

  const login = async (email, password) => {
    const res = await api.post('/api/auth/login/', { email, password });
    _accessToken = res.data.access;
    setUser(res.data.user);
    return res.data.user;
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout/');
    } catch {}
    _accessToken = null;
    setUser(null);
  };

  const updateUser = (data) => setUser((prev) => ({ ...prev, ...data }));

  return (
    <AuthContext.Provider
      value={{ user, loading, login, logout, updateUser, isAuthenticated: !!user }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
