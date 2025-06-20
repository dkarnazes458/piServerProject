/**
 * Hook for managing user modules and permissions
 */
import { useState, useEffect } from 'react';
import apiService from '../services/api';
import { getAvailableModules, isModuleAvailable } from '../modules/moduleRegistry';

export const useModules = (user) => {
  const [userModules, setUserModules] = useState([]);
  const [availableModules, setAvailableModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const isAdmin = user?.is_admin || false;

  useEffect(() => {
    if (user) {
      loadUserModules();
    }
  }, [user]);

  const loadUserModules = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiService.getUserModules();
      const modules = response.modules || [];
      
      setUserModules(modules);
      
      // Get available modules based on permissions
      const available = getAvailableModules(modules, isAdmin);
      setAvailableModules(available);
      
    } catch (err) {
      console.error('Failed to load user modules:', err);
      setError(err.message);
      // Set default available modules if API fails
      setAvailableModules([]);
    } finally {
      setLoading(false);
    }
  };

  const toggleModule = async (moduleId) => {
    try {
      await apiService.toggleUserModule(moduleId);
      await loadUserModules(); // Refresh modules after toggle
    } catch (err) {
      console.error('Failed to toggle module:', err);
      setError(err.message);
    }
  };

  const checkModuleAccess = (moduleName) => {
    return isModuleAvailable(moduleName, userModules, isAdmin);
  };

  return {
    userModules,
    availableModules,
    loading,
    error,
    toggleModule,
    checkModuleAccess,
    refreshModules: loadUserModules
  };
};