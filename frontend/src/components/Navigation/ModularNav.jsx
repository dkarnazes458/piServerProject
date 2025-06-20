/**
 * Modular Navigation Component
 * 
 * Renders navigation based on user's enabled modules and permissions
 */
import React, { useState } from 'react';
import { useModules } from '../../hooks/useModules';
import { loadModule } from '../../modules/moduleRegistry';
import './ModularNav.css';

const ModularNav = ({ user, onModuleSelect, currentModule }) => {
  const { availableModules, loading, error } = useModules(user);
  const [loadingModule, setLoadingModule] = useState(null);

  const handleModuleClick = async (module) => {
    if (loadingModule) return;
    
    try {
      setLoadingModule(module.name);
      
      // Load the module dynamically
      const loadedModule = await loadModule(module.name);
      
      // Notify parent component about module selection
      onModuleSelect(module.name, loadedModule);
      
    } catch (err) {
      console.error(`Failed to load module ${module.name}:`, err);
    } finally {
      setLoadingModule(null);
    }
  };

  const getModuleIcon = (iconName) => {
    // Map icon names to actual icons (you can replace with your icon library)
    const iconMap = {
      dashboard: '📊',
      boat: '⛵',
      map: '🗺️',
      tools: '🔧',
      wrench: '🔧',
      calendar: '📅',
      compass: '🧭',
      users: '👥',
      settings: '⚙️'
    };
    
    return iconMap[iconName] || '📄';
  };

  if (loading) {
    return (
      <nav className="modular-nav">
        <div className="nav-loading">Loading modules...</div>
      </nav>
    );
  }

  if (error) {
    return (
      <nav className="modular-nav">
        <div className="nav-error">Error loading modules: {error}</div>
      </nav>
    );
  }

  return (
    <nav className="modular-nav">
      <div className="nav-header">
        <h2>Sailor Utility</h2>
        <div className="user-info">
          <span className="user-name">{user?.first_name || user?.username}</span>
          {user?.is_admin && <span className="admin-badge">Admin</span>}
        </div>
      </div>
      
      <div className="nav-modules">
        {availableModules.map((module) => (
          <button
            key={module.name}
            className={`nav-module ${currentModule === module.name ? 'active' : ''} ${loadingModule === module.name ? 'loading' : ''}`}
            onClick={() => handleModuleClick(module)}
            disabled={loadingModule === module.name}
            title={module.description}
          >
            <span className="module-icon">{getModuleIcon(module.icon)}</span>
            <span className="module-name">{module.displayName}</span>
            {loadingModule === module.name && (
              <span className="loading-indicator">...</span>
            )}
          </button>
        ))}
      </div>
      
      <div className="nav-footer">
        <button className="nav-logout" onClick={() => onModuleSelect('logout')}>
          <span className="module-icon">🚪</span>
          <span className="module-name">Logout</span>
        </button>
      </div>
    </nav>
  );
};

export default ModularNav;