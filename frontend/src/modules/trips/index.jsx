/**
 * Trips Module
 * 
 * Trip logging and GPS tracking
 */
import React from 'react';
import '../shared.css';

const TripsModule = ({ user }) => {
  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Trip Logbook</h1>
        <p>Log and track your sailing trips with GPS support</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The trips module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>Trip logging and details</li>
            <li>GPS track upload and visualization</li>
            <li>Route planning</li>
            <li>Weather tracking</li>
            <li>Crew management</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TripsModule;