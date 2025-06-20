/**
 * Social Module
 * 
 * Crew network and communication
 */
import React from 'react';
import '../shared.css';

const SocialModule = ({ user }) => {
  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Crew Network</h1>
        <p>Connect with other sailors and crew members</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The social module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>Sailor profiles and networking</li>
            <li>Crew matching and recruitment</li>
            <li>Messaging and communication</li>
            <li>Experience sharing</li>
            <li>Community features</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SocialModule;