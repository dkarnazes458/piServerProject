/**
 * Boats Module
 * 
 * Fleet management and boat tracking
 */
import React from 'react';
import '../shared.css';

const BoatsModule = ({ user }) => {
  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Fleet Management</h1>
        <p>Manage your boats and fleet information</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The boats module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>Boat registration and details</li>
            <li>Fleet management</li>
            <li>Boat documentation</li>
            <li>Crew assignments</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default BoatsModule;