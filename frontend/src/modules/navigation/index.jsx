/**
 * Navigation Module
 * 
 * Weather and route planning
 */
import React from 'react';
import '../shared.css';

const NavigationModule = ({ user }) => {
  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Weather & Routes</h1>
        <p>Weather information and route planning tools</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The navigation module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>Weather forecasts and conditions</li>
            <li>Route planning and optimization</li>
            <li>Chart integration</li>
            <li>Tide and current information</li>
            <li>Navigation tools</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default NavigationModule;