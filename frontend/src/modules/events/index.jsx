/**
 * Events Module
 * 
 * Event management and calendar
 */
import React from 'react';
import '../shared.css';

const EventsModule = ({ user }) => {
  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Events Calendar</h1>
        <p>Manage sailing events, races, and gatherings</p>
      </header>
      
      <div className="module-content">
        <div className="placeholder-content">
          <h3>🚧 Under Development</h3>
          <p>The events module is currently being developed.</p>
          <p>This will include features for:</p>
          <ul>
            <li>Event creation and management</li>
            <li>Registration handling</li>
            <li>Calendar integration</li>
            <li>Participant tracking</li>
            <li>Event results and reports</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default EventsModule;