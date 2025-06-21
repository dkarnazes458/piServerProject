import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const EquipmentForm = ({ equipment, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    subcategory: '',
    brand: '',
    model: '',
    serial_number: '',
    purchase_date: '',
    purchase_price: '',
    warranty_expiry: '',
    boat_id: '',
    location_on_boat: '',
    condition: 'Good',
    is_operational: true,
    quantity: 1,
    notes: ''
  });
  const [boats, setBoats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const categories = [
    'Safety',
    'Navigation', 
    'Electronics',
    'Sail',
    'Rigging',
    'Engine',
    'Maintenance',
    'Galley',
    'Plumbing',
    'Electrical',
    'Deck Hardware',
    'Interior',
    'Tools',
    'Spare Parts',
    'Other'
  ];

  const conditions = ['Excellent', 'Good', 'Fair', 'Poor'];

  useEffect(() => {
    loadBoats();
    
    if (equipment) {
      setFormData({
        name: equipment.name || '',
        category: equipment.category || '',
        subcategory: equipment.subcategory || '',
        brand: equipment.brand || '',
        model: equipment.model || '',
        serial_number: equipment.serial_number || '',
        purchase_date: equipment.purchase_date || '',
        purchase_price: equipment.purchase_price || '',
        warranty_expiry: equipment.warranty_expiry || '',
        boat_id: equipment.boat_id || '',
        location_on_boat: equipment.location_on_boat || '',
        condition: equipment.condition || 'Good',
        is_operational: equipment.is_operational !== false,
        quantity: equipment.quantity || 1,
        notes: equipment.notes || ''
      });
    }
  }, [equipment]);

  const loadBoats = async () => {
    try {
      const response = await api.getBoats();
      setBoats(response.boats || []);
    } catch (err) {
      console.error('Error loading boats:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
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
        purchase_price: formData.purchase_price ? parseFloat(formData.purchase_price) : null,
        quantity: parseInt(formData.quantity) || 1,
        boat_id: formData.boat_id || null
      };

      // Remove empty strings
      Object.keys(submitData).forEach(key => {
        if (submitData[key] === '') {
          submitData[key] = null;
        }
      });

      let response;
      if (equipment) {
        response = await api.updateEquipment(equipment.id, submitData);
      } else {
        response = await api.createEquipment(submitData);
      }

      onSave(response.equipment || response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const calculateAge = () => {
    if (!formData.purchase_date) return null;
    
    const purchaseDate = new Date(formData.purchase_date);
    const today = new Date();
    const diffTime = Math.abs(today - purchaseDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 30) return `${diffDays} days old`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months old`;
    return `${Math.floor(diffDays / 365)} years old`;
  };

  const getWarrantyStatus = () => {
    if (!formData.warranty_expiry) return null;
    
    const expiryDate = new Date(formData.warranty_expiry);
    const today = new Date();
    const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysUntilExpiry < 0) return `Expired ${Math.abs(daysUntilExpiry)} days ago`;
    if (daysUntilExpiry === 0) return 'Expires today';
    return `${daysUntilExpiry} days remaining`;
  };

  return (
    <div className="equipment-form-container">
      <div className="form-header">
        <h2>{equipment ? 'Edit Equipment' : 'Add New Equipment'}</h2>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="equipment-form">
        <div className="form-section">
          <h3>Basic Information</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Equipment name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="category">Category</label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
              >
                <option value="">Select category...</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="subcategory">Subcategory</label>
              <input
                type="text"
                id="subcategory"
                name="subcategory"
                value={formData.subcategory}
                onChange={handleChange}
                placeholder="e.g. Communication, Life Jacket"
              />
            </div>

            <div className="form-group">
              <label htmlFor="condition">Condition</label>
              <select
                id="condition"
                name="condition"
                value={formData.condition}
                onChange={handleChange}
              >
                {conditions.map(condition => (
                  <option key={condition} value={condition}>{condition}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Product Details</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="brand">Brand</label>
              <input
                type="text"
                id="brand"
                name="brand"
                value={formData.brand}
                onChange={handleChange}
                placeholder="e.g. Garmin, Raymarine"
              />
            </div>

            <div className="form-group">
              <label htmlFor="model">Model</label>
              <input
                type="text"
                id="model"
                name="model"
                value={formData.model}
                onChange={handleChange}
                placeholder="Model number or name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="serial_number">Serial Number</label>
              <input
                type="text"
                id="serial_number"
                name="serial_number"
                value={formData.serial_number}
                onChange={handleChange}
                placeholder="Serial or ID number"
              />
            </div>

            <div className="form-group">
              <label htmlFor="quantity">Quantity</label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                min="1"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Purchase & Warranty</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="purchase_date">Purchase Date</label>
              <input
                type="date"
                id="purchase_date"
                name="purchase_date"
                value={formData.purchase_date}
                onChange={handleChange}
              />
              {formData.purchase_date && (
                <small className="form-hint">Age: {calculateAge()}</small>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="purchase_price">Purchase Price ($)</label>
              <input
                type="number"
                id="purchase_price"
                name="purchase_price"
                value={formData.purchase_price}
                onChange={handleChange}
                step="0.01"
                min="0"
                placeholder="0.00"
              />
            </div>

            <div className="form-group">
              <label htmlFor="warranty_expiry">Warranty Expiry</label>
              <input
                type="date"
                id="warranty_expiry"
                name="warranty_expiry"
                value={formData.warranty_expiry}
                onChange={handleChange}
              />
              {formData.warranty_expiry && (
                <small className="form-hint">Status: {getWarrantyStatus()}</small>
              )}
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Location</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="boat_id">Boat</label>
              <select
                id="boat_id"
                name="boat_id"
                value={formData.boat_id}
                onChange={handleChange}
              >
                <option value="">Not assigned to boat</option>
                {boats.map(boat => (
                  <option key={boat.id} value={boat.id}>{boat.name}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="location_on_boat">Location on Boat</label>
              <input
                type="text"
                id="location_on_boat"
                name="location_on_boat"
                value={formData.location_on_boat}
                onChange={handleChange}
                placeholder="e.g. Nav station, Port locker"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Status & Notes</h3>
          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="is_operational"
                checked={formData.is_operational}
                onChange={handleChange}
              />
              Equipment is operational
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notes</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows="4"
              placeholder="Additional notes, maintenance instructions, etc."
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
            {loading ? 'Saving...' : (equipment ? 'Update Equipment' : 'Add Equipment')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default EquipmentForm;