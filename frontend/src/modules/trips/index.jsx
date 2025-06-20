/**
 * Trips Module
 * 
 * Trip logging and GPS tracking
 */
import React, { useState, useEffect } from 'react';
import '../shared.css';
import './trips.css';
import TripForm from './components/TripForm';
import TripList from './components/TripList';
import TripDetail from './components/TripDetail';
import apiService from '../../services/api';

const TripsModule = ({ user }) => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentView, setCurrentView] = useState('list'); // list, form, detail
  const [selectedTrip, setSelectedTrip] = useState(null);

  useEffect(() => {
    loadTrips();
  }, []);

  const loadTrips = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await apiService.getTrips();
      setTrips(response.trips || []);
    } catch (err) {
      setError(err.message || 'Failed to load trips');
    } finally {
      setLoading(false);
    }
  };

  const handlePlanTrip = () => {
    setSelectedTrip(null);
    setCurrentView('form');
  };

  const handleEditTrip = (trip) => {
    setSelectedTrip(trip);
    setCurrentView('form');
  };

  const handleViewTrip = (trip) => {
    setSelectedTrip(trip);
    setCurrentView('detail');
  };

  const handleDeleteTrip = async (trip) => {
    try {
      await apiService.deleteTrip(trip.id);
      setTrips(trips.filter(t => t.id !== trip.id));
    } catch (err) {
      setError(err.message || 'Failed to delete trip');
    }
  };

  const handleSaveTrip = (savedTrip) => {
    if (selectedTrip) {
      // Update existing trip
      setTrips(trips.map(t => t.id === savedTrip.id ? savedTrip : t));
    } else {
      // Add new trip
      setTrips([...trips, savedTrip]);
    }
    setCurrentView('list');
    setSelectedTrip(null);
  };

  const handleCancel = () => {
    setCurrentView('list');
    setSelectedTrip(null);
  };

  // Calculate some quick stats
  const completedTrips = trips.filter(t => t.status === 'Completed').length;
  const plannedTrips = trips.filter(t => t.status === 'Planned').length;
  const inProgressTrips = trips.filter(t => t.status === 'In Progress').length;
  const totalDistance = trips
    .filter(t => t.distance_miles)
    .reduce((sum, t) => sum + (t.distance_miles || 0), 0);

  if (loading) {
    return (
      <div className="module-container">
        <div className="loading-state">
          <p>Loading trips...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Trip Logbook</h1>
        <p>Log and track your sailing trips with GPS support</p>
      </header>
      
      <div className="module-content">
        {error && (
          <div className="error-message">
            {error}
            <button 
              onClick={() => setError('')}
              style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}
            >
              ✕
            </button>
          </div>
        )}

        <div className="trips-container">
          {currentView === 'list' && (
            <>
              <div className="trips-header">
                <div>
                  <h2>My Trips ({trips.length})</h2>
                </div>
                <div className="trips-actions">
                  <button onClick={handlePlanTrip} className="btn-primary">
                    + Plan Trip
                  </button>
                  <button onClick={loadTrips} className="btn-secondary">
                    Refresh
                  </button>
                </div>
              </div>

              {/* Quick Stats */}
              {trips.length > 0 && (
                <div className="trip-stats">
                  <div className="stat-card">
                    <span className="stat-value">{completedTrips}</span>
                    <span className="stat-label">Completed</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-value">{plannedTrips}</span>
                    <span className="stat-label">Planned</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-value">{inProgressTrips}</span>
                    <span className="stat-label">In Progress</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-value">{totalDistance.toFixed(1)}</span>
                    <span className="stat-label">Total NM</span>
                  </div>
                </div>
              )}

              <TripList
                trips={trips}
                onEdit={handleEditTrip}
                onDelete={handleDeleteTrip}
                onView={handleViewTrip}
              />
            </>
          )}

          {currentView === 'form' && (
            <TripForm
              trip={selectedTrip}
              onSave={handleSaveTrip}
              onCancel={handleCancel}
            />
          )}

          {currentView === 'detail' && (
            <TripDetail
              trip={selectedTrip}
              onEdit={handleEditTrip}
              onClose={handleCancel}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default TripsModule;