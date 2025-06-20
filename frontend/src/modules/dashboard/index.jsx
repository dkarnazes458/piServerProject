/**
 * Dashboard Module
 * 
 * Main dashboard with overview and statistics
 */
import React from 'react';
import './Dashboard.css';
import '../shared.css';

const Dashboard = ({ user }) => {
  return (
    <div className="dashboard-module">
      <header className="module-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {user?.first_name || user?.username}!</p>
      </header>
      
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Recent Activity</h3>
          <p>No recent activity to display.</p>
        </div>
        
        <div className="dashboard-card">
          <h3>Quick Stats</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Boats</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Trips</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Equipment</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Events</span>
            </div>
          </div>
        </div>
        
        <div className="dashboard-card">
          <h3>Upcoming Events</h3>
          <p>No upcoming events scheduled.</p>
        </div>
        
        <div className="dashboard-card">
          <h3>Maintenance Reminders</h3>
          <p>No maintenance items due.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;