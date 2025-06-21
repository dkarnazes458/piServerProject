import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const MaintenanceDetail = ({ record, onEdit, onBack, onDelete }) => {
  const [relatedRecords, setRelatedRecords] = useState([]);
  const [loadingRelated, setLoadingRelated] = useState(false);
  const [boatName, setBoatName] = useState('');
  const [equipmentName, setEquipmentName] = useState('');

  useEffect(() => {
    if (record) {
      loadRelatedData();
      loadRelatedRecords();
    }
  }, [record]);

  const loadRelatedData = async () => {
    try {
      // Load boat name
      if (record.boat_id) {
        const boatsResponse = await api.getBoats();
        const boat = boatsResponse.boats?.find(b => b.id === record.boat_id);
        setBoatName(boat ? boat.name : 'Unknown Boat');
      }

      // Load equipment name
      if (record.equipment_id) {
        const equipmentResponse = await api.getEquipment();
        const equipment = equipmentResponse.equipment?.find(e => e.id === record.equipment_id);
        setEquipmentName(equipment ? equipment.name : 'Unknown Equipment');
      }
    } catch (err) {
      console.error('Error loading related data:', err);
    }
  };

  const loadRelatedRecords = async () => {
    try {
      setLoadingRelated(true);
      const response = await api.getMaintenance();
      
      // Find related maintenance records (same boat or equipment)
      const related = response.maintenance_records?.filter(r => 
        r.id !== record.id && (
          r.boat_id === record.boat_id ||
          (record.equipment_id && r.equipment_id === record.equipment_id)
        )
      ) || [];
      
      setRelatedRecords(related.slice(0, 5)); // Limit to 5 most recent
    } catch (err) {
      console.error('Error loading related records:', err);
    } finally {
      setLoadingRelated(false);
    }
  };

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
      case 'routine': return 'status-info';
      case 'repair': return 'status-warning';
      case 'replacement': return 'status-error';
      case 'inspection': return 'status-success';
      default: return 'status-neutral';
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${record.title}"? This action cannot be undone.`)) {
      try {
        await api.deleteMaintenance(record.id);
        onDelete();
      } catch (err) {
        alert('Error deleting maintenance record: ' + err.message);
      }
    }
  };

  const cost = formatCurrency(record.cost);

  return (
    <div className="maintenance-detail">
      <div className="detail-header">
        <div className="detail-title">
          <button onClick={onBack} className="btn-link back-button">
            ← Back to Maintenance List
          </button>
          <h1>{record.title || 'Maintenance Record'}</h1>
          <p className="maintenance-subtitle">
            {record.maintenance_type} • {formatDate(record.date_performed)}
          </p>
        </div>
        <div className="detail-actions">
          <button onClick={() => onEdit(record)} className="btn-primary">
            Edit Record
          </button>
          <button onClick={handleDelete} className="btn-danger">
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
                <label>Type:</label>
                <span className={`status ${getTypeClass(record.maintenance_type)}`}>
                  {record.maintenance_type || 'Not specified'}
                </span>
              </div>
              
              <div className="detail-item">
                <label>Date Performed:</label>
                <span>{formatDate(record.date_performed)}</span>
              </div>
              
              {record.performed_by && (
                <div className="detail-item">
                  <label>Performed By:</label>
                  <span>{record.performed_by}</span>
                </div>
              )}
              
              {record.next_maintenance_due && (
                <div className="detail-item">
                  <label>Next Maintenance Due:</label>
                  <span>{formatDate(record.next_maintenance_due)}</span>
                </div>
              )}
            </div>
          </div>

          {/* Boat & Equipment */}
          <div className="detail-section">
            <h3>Boat & Equipment</h3>
            <div className="detail-items">
              <div className="detail-item">
                <label>Boat:</label>
                <span>{boatName || 'Not specified'}</span>
              </div>
              
              {equipmentName && (
                <div className="detail-item">
                  <label>Equipment:</label>
                  <span>{equipmentName}</span>
                </div>
              )}
            </div>
          </div>

          {/* Cost & Time */}
          <div className="detail-section">
            <h3>Cost & Time</h3>
            <div className="detail-items">
              {cost && (
                <div className="detail-item">
                  <label>Cost:</label>
                  <span className="cost-value">{cost}</span>
                </div>
              )}
              
              {record.hours_spent && (
                <div className="detail-item">
                  <label>Hours Spent:</label>
                  <span>{record.hours_spent} hours</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="detail-section full-width">
          <h3>Description</h3>
          <div className="description-content">
            {record.description ? (
              record.description.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))
            ) : (
              <p>No description provided.</p>
            )}
          </div>
        </div>

        {/* Parts Used */}
        {record.parts_used && (
          <div className="detail-section full-width">
            <h3>Parts Used</h3>
            <div className="parts-content">
              {record.parts_used.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        )}

        {/* Notes */}
        {record.notes && (
          <div className="detail-section full-width">
            <h3>Additional Notes</h3>
            <div className="notes-content">
              {record.notes.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        )}

        {/* Related Maintenance Records */}
        <div className="detail-section full-width">
          <h3>Related Maintenance Records</h3>
          {loadingRelated ? (
            <div className="loading">Loading related records...</div>
          ) : relatedRecords.length === 0 ? (
            <div className="empty-state">
              <p>No related maintenance records found.</p>
            </div>
          ) : (
            <div className="related-records">
              {relatedRecords.map(relatedRecord => (
                <div key={relatedRecord.id} className="related-record">
                  <div className="related-header">
                    <h4>{relatedRecord.title || 'Maintenance Record'}</h4>
                    <span className="related-date">
                      {formatDate(relatedRecord.date_performed)}
                    </span>
                  </div>
                  <div className="related-details">
                    <span className={`related-type ${getTypeClass(relatedRecord.maintenance_type)}`}>
                      {relatedRecord.maintenance_type}
                    </span>
                    {relatedRecord.cost && (
                      <span className="related-cost">
                        {formatCurrency(relatedRecord.cost)}
                      </span>
                    )}
                  </div>
                  {relatedRecord.description && (
                    <p className="related-description">
                      {relatedRecord.description.length > 100 
                        ? relatedRecord.description.substring(0, 100) + '...'
                        : relatedRecord.description
                      }
                    </p>
                  )}
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
              <label>Days Since Maintenance:</label>
              <span>
                {record.date_performed 
                  ? Math.floor((new Date() - new Date(record.date_performed)) / (1000 * 60 * 60 * 24))
                  : 'Unknown'
                } days
              </span>
            </div>
            
            {record.next_maintenance_due && (
              <div className="stat-item">
                <label>Days Until Next Maintenance:</label>
                <span className={
                  new Date(record.next_maintenance_due) < new Date() 
                    ? 'status-error' 
                    : 'status-success'
                }>
                  {Math.floor((new Date(record.next_maintenance_due) - new Date()) / (1000 * 60 * 60 * 24))} days
                </span>
              </div>
            )}
            
            <div className="stat-item">
              <label>Related Records:</label>
              <span>{relatedRecords.length}</span>
            </div>
            
            {cost && (
              <div className="stat-item">
                <label>Total Cost:</label>
                <span className="cost-value">{cost}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MaintenanceDetail;