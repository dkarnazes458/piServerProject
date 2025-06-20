/**
 * Module Loader Component
 * 
 * Handles dynamic loading and rendering of modules
 */
import React, { useState, useEffect, Suspense } from 'react';
import { useModules } from '../hooks/useModules';

const ModuleLoader = ({ moduleName, user, ...props }) => {
  const [ModuleComponent, setModuleComponent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { checkModuleAccess } = useModules(user);

  useEffect(() => {
    loadModuleComponent();
  }, [moduleName]);

  const loadModuleComponent = async () => {
    if (!moduleName) {
      setLoading(false);
      return;
    }

    // Check if user has access to this module
    if (!checkModuleAccess(moduleName)) {
      setError('Access denied to this module');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Dynamic import based on module name
      const moduleImport = await import(`../modules/${moduleName}/index.jsx`);
      
      // Get the default export (main component)
      const Component = moduleImport.default;
      
      if (!Component) {
        throw new Error(`Module ${moduleName} does not export a default component`);
      }

      setModuleComponent(() => Component);
      
    } catch (err) {
      console.error(`Failed to load module ${moduleName}:`, err);
      setError(`Failed to load module: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="module-loading">
        <div className="loading-spinner"></div>
        <p>Loading {moduleName} module...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="module-error">
        <h3>Module Load Error</h3>
        <p>{error}</p>
        <button onClick={loadModuleComponent}>Retry</button>
      </div>
    );
  }

  if (!ModuleComponent) {
    return (
      <div className="module-placeholder">
        <p>No module selected</p>
      </div>
    );
  }

  return (
    <Suspense fallback={<div className="module-loading">Loading component...</div>}>
      <ModuleComponent user={user} {...props} />
    </Suspense>
  );
};

export default ModuleLoader;