/* eslint-disable no-unused-vars */
import { useState, useEffect } from 'react';
import { fetchLogs, fetchStats } from '../utils/api';

export const useLogs = (refreshInterval = 5000) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadLogs = async (serviceFilter = null) => {
    try {
      setLoading(true);
      const data = await fetchLogs(serviceFilter);
      setLogs(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
    const interval = setInterval(() => loadLogs(), refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  return { logs, loading, error, refetch: loadLogs };
};