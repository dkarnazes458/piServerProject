import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const EquipmentDetail = ({ equipment, onEdit, onBack, onDelete }) => {
  const [maintenanceHistory, setMaintenanceHistory] = useState([]);
  const [loadingMaintenance, setLoadingMaintenance] = useState(false);

  useEffect(() => {
    if (equipment) {
      loadMaintenanceHistory();
    }
  }, [equipment]);

  const loadMaintenanceHistory = async () => {
    try {
      setLoadingMaintenance(true);
      const response = await api.getMaintenance();
      // Filter maintenance records for this equipment
      const equipmentMaintenance = response.maintenance_records?.filter(
        record => record.equipment_id === equipment.id
      ) || [];
      setMaintenanceHistory(equipmentMaintenance);
    } catch (err) {
      console.error('Error loading maintenance history:', err);
    } finally {
      setLoadingMaintenance(false);
    }
  };

  const calculateAge = () => {
    if (!equipment.purchase_date) return null;
    
    const purchaseDate = new Date(equipment.purchase_date);
    const today = new Date();
    const diffTime = Math.abs(today - purchaseDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 30) return `${diffDays} days`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months`;
    return `${Math.floor(diffDays / 365)} years`;
  };

  const getWarrantyStatus = () => {
    if (!equipment.warranty_expiry) return null;
    
    const expiryDate = new Date(equipment.warranty_expiry);
    const today = new Date();
    const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysUntilExpiry < 0) {
      return { 
        text: `Expired ${Math.abs(daysUntilExpiry)} days ago`, 
        class: 'status-error' 
      };
    }
    if (daysUntilExpiry === 0) {
      return { text: 'Expires today', class: 'status-warning' };
    }
    if (daysUntilExpiry <= 30) {
      return { 
        text: `${daysUntilExpiry} days remaining`, 
        class: 'status-warning' 
      };
    }
    return { text: `${daysUntilExpiry} days remaining`, class: 'status-success' };
  };

  const getConditionClass = (condition) => {
    switch (condition?.toLowerCase()) {
      case 'excellent': return 'status-success';
      case 'good': return 'status-info';
      case 'fair': return 'status-warning';
      case 'poor': return 'status-error';
      default: return 'status-neutral';
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString();
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${equipment.name}"? This action cannot be undone.`)) {
      try {
        await api.deleteEquipment(equipment.id);
        onDelete();
      } catch (err) {
        alert('Error deleting equipment: ' + err.message);
      }
    }
  };

  const warranty = getWarrantyStatus();
  const age = calculateAge();

  return (
    <div className="equipment-detail">
      <div className="detail-header">
        <div className="detail-title">
          <button onClick={onBack} className="btn btn-link back-button">
            ← Back to Equipment List
          </button>
          <h1>{equipment.name}</h1>
          {equipment.brand && equipment.model && (
            <p className="equipment-subtitle">{equipment.brand} {equipment.model}</p>
          )}
        </div>
        <div className="detail-actions">
          <button onClick={() => onEdit(equipment)} className="btn btn-primary">
            Edit Equipment
          </button>
          <button onClick={handleDelete} className="btn btn-danger">
            Delete
          </button>
        </div>
      </div>

      <div className="detail-content">
        <div className="detail-grid">
          {/* Basic Information */}
          <div className="detail-section">
            <h3>Basic Information</h3>
            <div className="detail-items">
              <div className="detail-item">
                <label>Category:</label>
                <span>{equipment.category || 'Not specified'}</span>
              </div>
              
              {equipment.subcategory && (
                <div className="detail-item">
                  <label>Subcategory:</label>
                  <span>{equipment.subcategory}</span>
                </div>
              )}
              
              <div className="detail-item">
                <label>Condition:</label>
                <span className={`status ${getConditionClass(equipment.condition)}`}>
                  {equipment.condition || 'Not specified'}
                </span>
              </div>
              
              <div className="detail-item">
                <label>Operational:</label>
                <span className={`status ${equipment.is_operational ? 'status-success' : 'status-error'}`}>
                  {equipment.is_operational ? 'Yes' : 'No'}
                </span>
              </div>
              
              <div className="detail-item">
                <label>Quantity:</label>
                <span>{equipment.quantity || 1}</span>
              </div>
            </div>
          </div>

          {/* Product Details */}
          <div className="detail-section">
            <h3>Product Details</h3>
            <div className="detail-items">
              {equipment.brand && (
                <div className="detail-item">
                  <label>Brand:</label>
                  <span>{equipment.brand}</span>
                </div>
              )}
              
              {equipment.model && (
                <div className="detail-item">
                  <label>Model:</label>
                  <span>{equipment.model}</span>
                </div>
              )}
              
              {equipment.serial_number && (
                <div className="detail-item">
                  <label>Serial Number:</label>
                  <span>{equipment.serial_number}</span>
                </div>
              )}
            </div>
          </div>

          {/* Purchase Information */}
          <div className="detail-section">
            <h3>Purchase Information</h3>
            <div className="detail-items">
              <div className="detail-item">
                <label>Purchase Date:</label>
                <span>{formatDate(equipment.purchase_date)}</span>
                {age && <small className="detail-hint">({age} old)</small>}
              </div>
              
              {equipment.purchase_price && (
                <div className="detail-item">
                  <label>Purchase Price:</label>
                  <span>{formatCurrency(equipment.purchase_price)}</span>
                </div>
              )}
              
              <div className="detail-item">
                <label>Warranty Expiry:</label>
                <span>{formatDate(equipment.warranty_expiry)}</span>
                {warranty && (
                  <span className={`status ${warranty.class}`}>
                    {warranty.text}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Location */}
          <div className="detail-section">
            <h3>Location</h3>
            <div className="detail-items">
              <div className="detail-item">
                <label>Boat:</label>
                <span>{equipment.boat_name || 'Not assigned'}</span>
              </div>
              
              {equipment.location_on_boat && (
                <div className="detail-item">
                  <label>Location on Boat:</label>
                  <span>{equipment.location_on_boat}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Notes */}
        {equipment.notes && (
          <div className="detail-section full-width">
            <h3>Notes</h3>
            <div className="notes-content">
              {equipment.notes.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        )}

        {/* Maintenance History */}
        <div className="detail-section full-width">
          <h3>Maintenance History</h3>
          {loadingMaintenance ? (
            <div className="loading">Loading maintenance history...</div>
          ) : maintenanceHistory.length === 0 ? (
            <div className="empty-state">
              <p>No maintenance records found for this equipment.</p>
            </div>
          ) : (
            <div className="maintenance-history">
              {maintenanceHistory.map(record => (
                <div key={record.id} className="maintenance-record">
                  <div className="maintenance-header">
                    <h4>{record.title}</h4>
                    <span className="maintenance-date">
                      {formatDate(record.date_performed)}
                    </span>
                  </div>
                  <div className="maintenance-details">
                    <p>{record.description}</p>
                    {record.cost && (
                      <span className="maintenance-cost">
                        Cost: {formatCurrency(record.cost)}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Stats */}
        <div className="detail-section full-width">
          <h3>Quick Stats</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <label>Age:</label>
              <span>{age || 'Unknown'}</span>
            </div>
            
            <div className="stat-item">
              <label>Warranty Status:</label>
              <span className={warranty ? warranty.class : 'status-neutral'}>
                {warranty ? warranty.text : 'No warranty info'}
              </span>
            </div>
            
            <div className="stat-item">
              <label>Maintenance Records:</label>
              <span>{maintenanceHistory.length}</span>
            </div>
            
            {equipment.purchase_price && (
              <div className="stat-item">
                <label>Current Value:</label>
                <span>{formatCurrency(equipment.purchase_price)}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EquipmentDetail;