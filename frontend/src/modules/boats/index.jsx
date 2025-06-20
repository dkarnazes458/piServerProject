/**
 * Boats Module
 * 
 * Fleet management and boat tracking
 */
import React, { useState, useEffect } from 'react';
import '../shared.css';
import './boats.css';
import BoatForm from './components/BoatForm';
import BoatList from './components/BoatList';
import BoatDetail from './components/BoatDetail';
import apiService from '../../services/api';

const BoatsModule = ({ user }) => {
  const [boats, setBoats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentView, setCurrentView] = useState('list'); // list, form, detail
  const [selectedBoat, setSelectedBoat] = useState(null);

  useEffect(() => {
    loadBoats();
  }, []);

  const loadBoats = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await apiService.getBoats();
      setBoats(response.boats || []);
    } catch (err) {
      setError(err.message || 'Failed to load boats');
    } finally {
      setLoading(false);
    }
  };

  const handleAddBoat = () => {
    setSelectedBoat(null);
    setCurrentView('form');
  };

  const handleEditBoat = (boat) => {
    setSelectedBoat(boat);
    setCurrentView('form');
  };

  const handleViewBoat = (boat) => {
    setSelectedBoat(boat);
    setCurrentView('detail');
  };

  const handleDeleteBoat = async (boat) => {
    try {
      await apiService.deleteBoat(boat.id);
      setBoats(boats.filter(b => b.id !== boat.id));
    } catch (err) {
      setError(err.message || 'Failed to delete boat');
    }
  };

  const handleSaveBoat = (savedBoat) => {
    if (selectedBoat) {
      // Update existing boat
      setBoats(boats.map(b => b.id === savedBoat.id ? savedBoat : b));
    } else {
      // Add new boat
      setBoats([...boats, savedBoat]);
    }
    setCurrentView('list');
    setSelectedBoat(null);
  };

  const handleCancel = () => {
    setCurrentView('list');
    setSelectedBoat(null);
  };

  if (loading) {
    return (
      <div className="module-container">
        <div className="loading-state">
          <p>Loading boats...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="module-container">
      <header className="module-header">
        <h1>Fleet Management</h1>
        <p>Manage your boats and fleet information</p>
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

        <div className="boats-container">
          {currentView === 'list' && (
            <>
              <div className="boats-header">
                <div>
                  <h2>My Boats ({boats.length})</h2>
                </div>
                <div className="boats-actions">
                  <button onClick={handleAddBoat} className="btn-primary">
                    + Add Boat
                  </button>
                  <button onClick={loadBoats} className="btn-secondary">
                    Refresh
                  </button>
                </div>
              </div>

              <BoatList
                boats={boats}
                onEdit={handleEditBoat}
                onDelete={handleDeleteBoat}
                onView={handleViewBoat}
              />
            </>
          )}

          {currentView === 'form' && (
            <BoatForm
              boat={selectedBoat}
              onSave={handleSaveBoat}
              onCancel={handleCancel}
            />
          )}

          {currentView === 'detail' && (
            <BoatDetail
              boat={selectedBoat}
              onEdit={handleEditBoat}
              onClose={handleCancel}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default BoatsModule;