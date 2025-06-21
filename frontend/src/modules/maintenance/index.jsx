/**
 * Maintenance Module
 * 
 * Maintenance record tracking and scheduling
 */
import React, { useState, useEffect } from 'react';
import '../shared.css';
import './maintenance.css';
import MaintenanceForm from './components/MaintenanceForm';
import MaintenanceList from './components/MaintenanceList';
import MaintenanceDetail from './components/MaintenanceDetail';
import apiService from '../../services/api';

const MaintenanceModule = ({ user }) => {
  const [maintenanceRecords, setMaintenanceRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentView, setCurrentView] = useState('list'); // list, form, detail
  const [selectedRecord, setSelectedRecord] = useState(null);

  useEffect(() => {
    loadMaintenanceRecords();
  }, []);

  const loadMaintenanceRecords = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await apiService.getMaintenance();
      setMaintenanceRecords(response.maintenance_records || []);
    } catch (err) {
      setError(err.message || 'Failed to load maintenance records');
    } finally {
      setLoading(false);
    }
  };

  const handleAddRecord = () => {
    setSelectedRecord(null);
    setCurrentView('form');
  };

  const handleEditRecord = (record) => {
    setSelectedRecord(record);
    setCurrentView('form');
  };

  const handleViewRecord = (record) => {
    setSelectedRecord(record);
    setCurrentView('detail');
  };

  const handleDeleteRecord = async (record) => {
    try {
      await apiService.deleteMaintenance(record.id);
      setMaintenanceRecords(maintenanceRecords.filter(r => r.id !== record.id));
    } catch (err) {
      setError(err.message || 'Failed to delete maintenance record');
    }
  };

  const handleSaveRecord = (savedRecord) => {
    if (selectedRecord) {
      // Update existing record
      setMaintenanceRecords(maintenanceRecords.map(r => r.id === savedRecord.id ? savedRecord : r));
    } else {
      // Add new record
      setMaintenanceRecords([...maintenanceRecords, savedRecord]);
    }
    setCurrentView('list');
    setSelectedRecord(null);
  };

  const handleCancel = () => {
    setCurrentView('list');
    setSelectedRecord(null);
  };

  if (loading) {
    return (
      <div className="maintenance-container">
        <div className="loading-state">
          <p>Loading maintenance records...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="maintenance-container">
      <header className="module-header">
        <h1>Maintenance Log</h1>
        <p>Track and schedule boat maintenance</p>
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

        <div className="maintenance-content">
          {currentView === 'list' && (
            <MaintenanceList
              records={maintenanceRecords}
              onEdit={handleEditRecord}
              onDelete={handleDeleteRecord}
              onView={handleViewRecord}
              onAdd={handleAddRecord}
              onRefresh={loadMaintenanceRecords}
            />
          )}

          {currentView === 'form' && (
            <MaintenanceForm
              record={selectedRecord}
              onSave={handleSaveRecord}
              onCancel={handleCancel}
            />
          )}

          {currentView === 'detail' && (
            <MaintenanceDetail
              record={selectedRecord}
              onEdit={handleEditRecord}
              onClose={handleCancel}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default MaintenanceModule;