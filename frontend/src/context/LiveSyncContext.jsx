import React, { createContext, useContext, useEffect, useRef } from 'react';
import { api } from '../api/client';
import { useAuth } from './AuthContext';

const LiveSyncContext = createContext(null);

export function LiveSyncProvider({ children }) {
  const { isAuthenticated } = useAuth();
  const listenersRef = useRef(new Set());
  const timerRef = useRef(null);

  const subscribe = (callback) => {
    listenersRef.current.add(callback);
    return () => listenersRef.current.delete(callback);
  };

  const triggerSync = (type = 'general', data = null) => {
    listenersRef.current.forEach((cb) => {
      try {
        cb({ type, data, timestamp: Date.now() });
      } catch (err) {
        console.error("LiveSync callback error:", err);
      }
    });
  };

  useEffect(() => {
    if (!isAuthenticated) return;

    // Periodic heartbeat poll (every 15s) to check updates
    const pollUpdates = async () => {
      if (document.hidden) return; // Don't poll if user is on another tab
      try {
        // Ping overview or health to trigger freshness
        await api.getSchoolOverview();
        triggerSync('heartbeat');
      } catch (err) {
        // Graceful silent fallback
      }
    };

    timerRef.current = setInterval(pollUpdates, 15000);

    const handleVisibility = () => {
      if (!document.hidden) {
        pollUpdates();
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      document.removeEventListener('visibilitychange', handleVisibility);
    };
  }, [isAuthenticated]);

  return (
    <LiveSyncContext.Provider value={{ triggerSync, subscribe }}>
      {children}
    </LiveSyncContext.Provider>
  );
}

export function useLiveSync() {
  const context = useContext(LiveSyncContext);
  if (!context) {
    return {
      triggerSync: () => {},
      subscribe: () => () => {},
    };
  }
  return context;
}
