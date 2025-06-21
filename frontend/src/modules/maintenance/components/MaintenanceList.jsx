import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const MaintenanceList = ({ records, onSelect, onEdit, onAdd, onRefresh }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [boatFilter, setBoatFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date_performed');
  const [boats, setBoats] = useState([]);

  useEffect(() => {
    loadBoats();
  }, []);

  const loadBoats = async () => {
    try {
      const response = await api.getBoats();
      setBoats(response.boats || []);
    } catch (err) {
      console.error('Error loading boats:', err);
    }
  };

  const handleDelete = async (id, title) => {
    if (window.confirm(`Are you sure you want to delete "${title}"? This action cannot be undone.`)) {
      try {
        await api.deleteMaintenance(id);
        // Trigger parent reload
        window.location.reload();
      } catch (err) {
        alert('Error deleting maintenance record: ' + err.message);
      }
    }
  };

  const getMaintenanceTypes = () => {
    const types = [...new Set(records.map(record => record.maintenance_type).filter(Boolean))];
    return types.sort();
  };

  const getBoatName = (boatId) => {
    const boat = boats.find(b => b.id === boatId);
    return boat ? boat.name : 'Unknown Boat';
  };

  const filteredRecords = records
    .filter(record => {
      const matchesSearch = !searchTerm || 
        record.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.performed_by?.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesType = typeFilter === 'all' || record.maintenance_type === typeFilter;
      const matchesBoat = boatFilter === 'all' || record.boat_id === parseInt(boatFilter);
      
      return matchesSearch && matchesType && matchesBoat;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date_performed':
          return new Date(b.date_performed || 0) - new Date(a.date_performed || 0);
        case 'title':
          return (a.title || '').localeCompare(b.title || '');
        case 'cost':
          return (b.cost || 0) - (a.cost || 0);
        case 'maintenance_type':
          return (a.maintenance_type || '').localeCompare(b.maintenance_type || '');
        default:
          return 0;
      }
    });

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (amount) => {
    if (!amount) return null;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const getTypeClass = (type) => {
    switch (type?.toLowerCase()) {
      case 'routine': return 'type-routine';
      case 'repair': return 'type-repair';
      case 'replacement': return 'type-replacement';
      case 'inspection': return 'type-inspection';
      default: return 'type-other';
    }
  };

  if (loading) {
    return (
      <div className="maintenance-list loading">
        <div className="loading-spinner">Loading maintenance records...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="maintenance-list error">
        <div className="error-message">
          <p>Error loading maintenance records: {error}</p>
          <button onClick={() => window.location.reload()} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="maintenance-list">
      <div className="list-header">
        <div className="list-title">
          <h2>Maintenance Records</h2>
          <span className="item-count">{filteredRecords.length} records</span>
        </div>
      </div>

      <div className="list-controls">
        <div className="controls-row">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search maintenance records..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          <div className="controls-buttons">
            <button onClick={onAdd} className="add-maintenance-btn">
              + Add Record
            </button>
            <button onClick={onRefresh} className="refresh-btn">
              Refresh
            </button>
          </div>
        </div>
        
        <div className="filter-controls">
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Types</option>
            {getMaintenanceTypes().map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
          
          <select
            value={boatFilter}
            onChange={(e) => setBoatFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Boats</option>
            {boats.map(boat => (
              <option key={boat.id} value={boat.id}>{boat.name}</option>
            ))}
          </select>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="date_performed">Sort by Date</option>
            <option value="title">Sort by Title</option>
            <option value="cost">Sort by Cost</option>
            <option value="maintenance_type">Sort by Type</option>
          </select>
        </div>
      </div>

      {filteredRecords.length === 0 ? (
        <div className="empty-state">
          <p>No maintenance records found.</p>
          {searchTerm || typeFilter !== 'all' || boatFilter !== 'all' ? (
            <p>Try adjusting your search or filters.</p>
          ) : (
            <p>Add your first maintenance record to get started.</p>
          )}
        </div>
      ) : (
        <div className="maintenance-grid">
          {filteredRecords.map(record => {
            const cost = formatCurrency(record.cost);
            
            return (
              <div key={record.id} className="maintenance-card">
                <div className="maintenance-header">
                  <h3 onClick={() => onSelect(record)} className="maintenance-title">
                    {record.title || record.description?.substring(0, 50) + '...' || 'Maintenance Record'}
                  </h3>
                  <div className="maintenance-actions">
                    <button 
                      onClick={() => onEdit(record)}
                      className="btn-sm btn-secondary"
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button 
                      onClick={() => handleDelete(record.id, record.title || 'maintenance record')}
                      className="btn-sm btn-danger"
                      title="Delete"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
                
                <div className="maintenance-details">
                  <div className="maintenance-meta">
                    <span className="maintenance-date">
                      <strong>Date:</strong> {formatDate(record.date_performed)}
                    </span>
                    
                    {record.maintenance_type && (
                      <span className={`maintenance-type ${getTypeClass(record.maintenance_type)}`}>
                        {record.maintenance_type}
                      </span>
                    )}
                  </div>
                  
                  <div className="maintenance-boat">
                    <span className="boat-info">
                      🚢 {getBoatName(record.boat_id)}
                    </span>
                  </div>
                  
                  {record.performed_by && (
                    <div className="performed-by">
                      <strong>Performed by:</strong> {record.performed_by}
                    </div>
                  )}
                  
                  {record.description && (
                    <div className="maintenance-description">
                      {record.description.length > 100 
                        ? record.description.substring(0, 100) + '...'
                        : record.description
                      }
                    </div>
                  )}
                  
                  <div className="maintenance-bottom">
                    {cost && (
                      <div className="maintenance-cost">
                        <strong>Cost:</strong> {cost}
                      </div>
                    )}
                    
                    {record.hours_spent && (
                      <div className="maintenance-hours">
                        <strong>Hours:</strong> {record.hours_spent}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default MaintenanceList;