import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const EquipmentList = ({ onSelect, onEdit, onAdd }) => {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [conditionFilter, setConditionFilter] = useState('all');
  const [sortBy, setSortBy] = useState('name');

  useEffect(() => {
    loadEquipment();
  }, []);

  const loadEquipment = async () => {
    try {
      setLoading(true);
      const response = await api.getEquipment();
      setEquipment(response.equipment || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (window.confirm(`Are you sure you want to delete "${name}"? This action cannot be undone.`)) {
      try {
        await api.deleteEquipment(id);
        await loadEquipment();
      } catch (err) {
        alert('Error deleting equipment: ' + err.message);
      }
    }
  };

  const getCategories = () => {
    const categories = [...new Set(equipment.map(item => item.category).filter(Boolean))];
    return categories.sort();
  };

  const getConditions = () => {
    const conditions = [...new Set(equipment.map(item => item.condition).filter(Boolean))];
    return conditions.sort();
  };

  const filteredEquipment = equipment
    .filter(item => {
      const matchesSearch = !searchTerm || 
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.brand?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.model?.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesCategory = categoryFilter === 'all' || item.category === categoryFilter;
      const matchesCondition = conditionFilter === 'all' || item.condition === conditionFilter;
      
      return matchesSearch && matchesCategory && matchesCondition;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'category':
          return (a.category || '').localeCompare(b.category || '');
        case 'condition':
          return (a.condition || '').localeCompare(b.condition || '');
        case 'purchase_date':
          return new Date(b.purchase_date || 0) - new Date(a.purchase_date || 0);
        case 'value':
          return (b.purchase_price || 0) - (a.purchase_price || 0);
        default:
          return 0;
      }
    });

  const getWarrantyStatus = (item) => {
    if (!item.warranty_expiry) return null;
    
    const expiryDate = new Date(item.warranty_expiry);
    const today = new Date();
    const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysUntilExpiry < 0) return { status: 'expired', text: 'Expired', class: 'status-error' };
    if (daysUntilExpiry <= 30) return { status: 'expiring', text: `${daysUntilExpiry} days`, class: 'status-warning' };
    return { status: 'valid', text: 'Valid', class: 'status-success' };
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

  if (loading) {
    return (
      <div className="equipment-list loading">
        <div className="loading-spinner">Loading equipment...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="equipment-list error">
        <div className="error-message">
          <p>Error loading equipment: {error}</p>
          <button onClick={loadEquipment} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="equipment-list">
      <div className="list-header">
        <div className="list-title">
          <h2>Equipment Inventory</h2>
          <span className="item-count">{filteredEquipment.length} items</span>
        </div>
        <button onClick={onAdd} className="btn btn-primary">
          Add Equipment
        </button>
      </div>

      <div className="list-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search equipment..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-controls">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Categories</option>
            {getCategories().map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
          
          <select
            value={conditionFilter}
            onChange={(e) => setConditionFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Conditions</option>
            {getConditions().map(condition => (
              <option key={condition} value={condition}>{condition}</option>
            ))}
          </select>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="name">Sort by Name</option>
            <option value="category">Sort by Category</option>
            <option value="condition">Sort by Condition</option>
            <option value="purchase_date">Sort by Purchase Date</option>
            <option value="value">Sort by Value</option>
          </select>
        </div>
      </div>

      {filteredEquipment.length === 0 ? (
        <div className="empty-state">
          <p>No equipment found.</p>
          {searchTerm || categoryFilter !== 'all' || conditionFilter !== 'all' ? (
            <p>Try adjusting your search or filters.</p>
          ) : (
            <p>Add your first piece of equipment to get started.</p>
          )}
        </div>
      ) : (
        <div className="equipment-grid">
          {filteredEquipment.map(item => {
            const warranty = getWarrantyStatus(item);
            
            return (
              <div key={item.id} className="equipment-card">
                <div className="equipment-header">
                  <h3 onClick={() => onSelect(item)} className="equipment-name">
                    {item.name}
                  </h3>
                  <div className="equipment-actions">
                    <button 
                      onClick={() => onEdit(item)}
                      className="btn btn-sm btn-secondary"
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button 
                      onClick={() => handleDelete(item.id, item.name)}
                      className="btn btn-sm btn-danger"
                      title="Delete"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
                
                <div className="equipment-details">
                  {item.brand && item.model && (
                    <p className="equipment-model">{item.brand} {item.model}</p>
                  )}
                  
                  <div className="equipment-meta">
                    {item.category && (
                      <span className="meta-item">
                        <strong>Category:</strong> {item.category}
                      </span>
                    )}
                    
                    {item.condition && (
                      <span className={`status ${getConditionClass(item.condition)}`}>
                        {item.condition}
                      </span>
                    )}
                    
                    {warranty && (
                      <span className={`status ${warranty.class}`}>
                        Warranty: {warranty.text}
                      </span>
                    )}
                  </div>
                  
                  <div className="equipment-location">
                    {item.boat_name && (
                      <span className="location-info">
                        📍 {item.boat_name}
                        {item.location_on_boat && ` - ${item.location_on_boat}`}
                      </span>
                    )}
                  </div>
                  
                  {item.purchase_price && (
                    <div className="equipment-value">
                      <strong>Value:</strong> ${item.purchase_price.toLocaleString()}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default EquipmentList;