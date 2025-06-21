import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const MaintenanceForm = ({ record, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    boat_id: '',
    equipment_id: '',
    maintenance_type: 'Routine',
    description: '',
    date_performed: '',
    performed_by: '',
    cost: '',
    hours_spent: '',
    next_maintenance_due: '',
    parts_used: '',
    notes: ''
  });
  const [boats, setBoats] = useState([]);
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const maintenanceTypes = [
    'Routine',
    'Repair', 
    'Replacement',
    'Inspection',
    'Cleaning',
    'Upgrade',
    'Emergency',
    'Preventive',
    'Other'
  ];

  useEffect(() => {
    loadBoats();
    loadEquipment();
    
    if (record) {
      setFormData({
        title: record.title || '',
        boat_id: record.boat_id || '',
        equipment_id: record.equipment_id || '',
        maintenance_type: record.maintenance_type || 'Routine',
        description: record.description || '',
        date_performed: record.date_performed || '',
        performed_by: record.performed_by || '',
        cost: record.cost || '',
        hours_spent: record.hours_spent || '',
        next_maintenance_due: record.next_maintenance_due || '',
        parts_used: record.parts_used || '',
        notes: record.notes || ''
      });
    }
  }, [record]);

  const loadBoats = async () => {
    try {
      const response = await api.getBoats();
      setBoats(response.boats || []);
    } catch (err) {
      console.error('Error loading boats:', err);
    }
  };

  const loadEquipment = async () => {
    try {
      const response = await api.getEquipment();
      setEquipment(response.equipment || []);
    } catch (err) {
      console.error('Error loading equipment:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert numeric fields
      const submitData = {
        ...formData,
        cost: formData.cost ? parseFloat(formData.cost) : null,
        hours_spent: formData.hours_spent ? parseFloat(formData.hours_spent) : null,
        boat_id: formData.boat_id || null,
        equipment_id: formData.equipment_id || null
      };

      // Remove empty strings
      Object.keys(submitData).forEach(key => {
        if (submitData[key] === '') {
          submitData[key] = null;
        }
      });

      let response;
      if (record) {
        response = await api.updateMaintenance(record.id, submitData);
      } else {
        response = await api.createMaintenance(submitData);
      }

      onSave(response.maintenance_record || response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredEquipment = () => {
    if (!formData.boat_id) return equipment;
    return equipment.filter(item => 
      !item.boat_id || item.boat_id === parseInt(formData.boat_id)
    );
  };

  return (
    <div className="maintenance-form-container">
      <div className="form-header">
        <h2>{record ? 'Edit Maintenance Record' : 'Add New Maintenance Record'}</h2>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="maintenance-form">
        <div className="form-section">
          <h3>Basic Information</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="title">Title *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="e.g. Oil Change, Sail Repair"
              />
            </div>

            <div className="form-group">
              <label htmlFor="maintenance_type">Type</label>
              <select
                id="maintenance_type"
                name="maintenance_type"
                value={formData.maintenance_type}
                onChange={handleChange}
              >
                {maintenanceTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="date_performed">Date Performed *</label>
              <input
                type="date"
                id="date_performed"
                name="date_performed"
                value={formData.date_performed}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="performed_by">Performed By</label>
              <input
                type="text"
                id="performed_by"
                name="performed_by"
                value={formData.performed_by}
                onChange={handleChange}
                placeholder="Name or service provider"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Boat & Equipment</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="boat_id">Boat *</label>
              <select
                id="boat_id"
                name="boat_id"
                value={formData.boat_id}
                onChange={handleChange}
                required
              >
                <option value="">Select boat...</option>
                {boats.map(boat => (
                  <option key={boat.id} value={boat.id}>{boat.name}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="equipment_id">Equipment (Optional)</label>
              <select
                id="equipment_id"
                name="equipment_id"
                value={formData.equipment_id}
                onChange={handleChange}
              >
                <option value="">No specific equipment</option>
                {getFilteredEquipment().map(item => (
                  <option key={item.id} value={item.id}>{item.name}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Description</h3>
          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              required
              placeholder="Detailed description of the maintenance work performed..."
            />
          </div>
        </div>

        <div className="form-section">
          <h3>Cost & Time</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="cost">Cost ($)</label>
              <input
                type="number"
                id="cost"
                name="cost"
                value={formData.cost}
                onChange={handleChange}
                step="0.01"
                min="0"
                placeholder="0.00"
              />
            </div>

            <div className="form-group">
              <label htmlFor="hours_spent">Hours Spent</label>
              <input
                type="number"
                id="hours_spent"
                name="hours_spent"
                value={formData.hours_spent}
                onChange={handleChange}
                step="0.5"
                min="0"
                placeholder="0.0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="next_maintenance_due">Next Maintenance Due</label>
              <input
                type="date"
                id="next_maintenance_due"
                name="next_maintenance_due"
                value={formData.next_maintenance_due}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Parts & Notes</h3>
          <div className="form-group">
            <label htmlFor="parts_used">Parts Used</label>
            <textarea
              id="parts_used"
              name="parts_used"
              value={formData.parts_used}
              onChange={handleChange}
              rows="3"
              placeholder="List of parts, part numbers, suppliers, etc."
            />
          </div>

          <div className="form-group">
            <label htmlFor="notes">Additional Notes</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows="3"
              placeholder="Any additional notes, recommendations, or observations..."
            />
          </div>
        </div>

        <div className="form-actions">
          <button 
            type="button" 
            onClick={onCancel}
            className="btn-secondary"
            disabled={loading}
          >
            Cancel
          </button>
          <button 
            type="submit"
            className="btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : (record ? 'Update Record' : 'Add Record')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default MaintenanceForm;