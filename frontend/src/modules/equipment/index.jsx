/**
 * Equipment Module
 * 
 * Equipment inventory and tracking
 */
import React from 'react';
import '../shared.css';

const EquipmentModule = ({ user }) => {
  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Equipment Tracker</h1>
        <p>Manage your sailing equipment and inventory</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The equipment module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>Equipment catalog and inventory</li>
            <li>Condition tracking</li>
            <li>Warranty management</li>
            <li>Maintenance scheduling</li>
            <li>Location tracking</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default EquipmentModule;