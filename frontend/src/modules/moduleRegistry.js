/**
 * Module Registry for Dynamic Loading
 * 
 * This file defines all available modules and provides
 * dynamic import functionality for the modular architecture.
 */

// Module definitions with metadata
export const MODULE_DEFINITIONS = {
  dashboard: {
    name: 'dashboard',
    displayName: 'Dashboard',
    icon: 'dashboard',
    description: 'Main dashboard with overview and statistics',
    path: '/dashboard',
    component: () => import('./dashboard/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  boats: {
    name: 'boats',
    displayName: 'Fleet Management',
    icon: 'boat',
    description: 'Manage your boats and fleet information',
    path: '/boats',
    component: () => import('./boats/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  trips: {
    name: 'trips',
    displayName: 'Trip Logbook',
    icon: 'map',
    description: 'Log and track your sailing trips with GPS support',
    path: '/trips',
    component: () => import('./trips/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  equipment: {
    name: 'equipment',
    displayName: 'Equipment Tracker',
    icon: 'tools',
    description: 'Manage your sailing equipment and inventory',
    path: '/equipment',
    component: () => import('./equipment/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  maintenance: {
    name: 'maintenance',
    displayName: 'Maintenance Log',
    icon: 'wrench',
    description: 'Track maintenance records and schedules',
    path: '/maintenance',
    component: () => import('./maintenance/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  events: {
    name: 'events',
    displayName: 'Events Calendar',
    icon: 'calendar',
    description: 'Manage sailing events, races, and gatherings',
    path: '/events',
    component: () => import('./events/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  navigation: {
    name: 'navigation',
    displayName: 'Weather & Routes',
    icon: 'compass',
    description: 'Weather information and route planning tools',
    path: '/navigation',
    component: () => import('./navigation/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  social: {
    name: 'social',
    displayName: 'Crew Network',
    icon: 'users',
    description: 'Connect with other sailors and crew members',
    path: '/social',
    component: () => import('./social/index.jsx'),
    requiresAuth: true,
    adminOnly: false
  },
  admin: {
    name: 'admin',
    displayName: 'Admin Panel',
    icon: 'settings',
    description: 'System administration and user management',
    path: '/admin',
    component: () => import('./admin/index.jsx'),
    requiresAuth: true,
    adminOnly: true
  }
};

/**
 * Load a module dynamically
 * @param {string} moduleName - Name of the module to load
 * @returns {Promise} - Promise that resolves to the module component
 */
export const loadModule = async (moduleName) => {
  const moduleConfig = MODULE_DEFINITIONS[moduleName];
  
  if (!moduleConfig) {
    throw new Error(`Module '${moduleName}' not found in registry`);
  }
  
  try {
    const moduleExports = await moduleConfig.component();
    return {
      ...moduleConfig,
      Component: moduleExports.default,
      ...moduleExports
    };
  } catch (error) {
    console.error(`Failed to load module '${moduleName}':`, error);
    throw error;
  }
};

/**
 * Get all available modules for a user
 * @param {Object} userModules - User's enabled modules from API
 * @param {boolean} isAdmin - Whether user is admin
 * @returns {Array} - Array of available module configs
 */
export const getAvailableModules = (userModules = [], isAdmin = false) => {
  return Object.values(MODULE_DEFINITIONS)
    .filter(module => {
      // Filter out admin-only modules for non-admin users
      if (module.adminOnly && !isAdmin) {
        return false;
      }
      
      // Check if user has permission for this module
      return userModules.some(userModule => 
        userModule.name === module.name && userModule.is_enabled
      );
    })
    .sort((a, b) => {
      // Sort by display name
      return a.displayName.localeCompare(b.displayName);
    });
};

/**
 * Get module definition by name
 * @param {string} moduleName - Name of the module
 * @returns {Object|null} - Module definition or null if not found
 */
export const getModuleDefinition = (moduleName) => {
  return MODULE_DEFINITIONS[moduleName] || null;
};

/**
 * Check if a module is available for a user
 * @param {string} moduleName - Name of the module
 * @param {Array} userModules - User's enabled modules
 * @param {boolean} isAdmin - Whether user is admin
 * @returns {boolean} - Whether module is available
 */
export const isModuleAvailable = (moduleName, userModules = [], isAdmin = false) => {
  const moduleConfig = MODULE_DEFINITIONS[moduleName];
  
  if (!moduleConfig) {
    return false;
  }
  
  if (moduleConfig.adminOnly && !isAdmin) {
    return false;
  }
  
  return userModules.some(userModule => 
    userModule.name === moduleName && userModule.is_enabled
  );
};