/**
 * Admin Module
 * 
 * System administration and user management
 */
import React from 'react';
import '../shared.css';

const AdminModule = ({ user }) => {
  if (!user?.is_admin) {
    return (
      <div className="module-container">
        <div className="module-content">
          <div className="access-denied">
            <h3>🔒 Access Denied</h3>
            <p>You do not have administrator privileges to access this module.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Admin Panel</h1>
        <p>System administration and user management</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The admin module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>User management and permissions</li>
            <li>Module configuration</li>
            <li>System monitoring</li>
            <li>Data management and backups</li>
            <li>Security settings</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AdminModule;