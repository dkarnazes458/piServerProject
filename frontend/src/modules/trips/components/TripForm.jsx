import React, { useState, useEffect } from 'react';
import apiService from '../../../services/api';

const TripForm = ({ trip = null, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    trip_type: 'Leisure',
    boat_id: '',
    start_date: '',
    end_date: '',
    planned_duration_hours: '',
    start_location: '',
    end_location: '',
    start_latitude: '',
    start_longitude: '',
    end_latitude: '',
    end_longitude: '',
    status: 'Planned',
    purpose: '',
    difficulty_level: 'Moderate',
    emergency_contact: '',
    float_plan_filed: false,
    float_plan_with: '',
    safety_equipment_check: false,
    notes: ''
  });
  
  const [boats, setBoats] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBoats();
  }, []);

  useEffect(() => {
    if (trip) {
      setFormData({
        name: trip.name || '',
        description: trip.description || '',
        trip_type: trip.trip_type || 'Leisure',
        boat_id: trip.boat_id || '',
        start_date: trip.start_date ? trip.start_date.substring(0, 16) : '',
        end_date: trip.end_date ? trip.end_date.substring(0, 16) : '',
        planned_duration_hours: trip.planned_duration_hours || '',
        start_location: trip.start_location || '',
        end_location: trip.end_location || '',
        start_latitude: trip.start_latitude || '',
        start_longitude: trip.start_longitude || '',
        end_latitude: trip.end_latitude || '',
        end_longitude: trip.end_longitude || '',
        status: trip.status || 'Planned',
        purpose: trip.purpose || '',
        difficulty_level: trip.difficulty_level || 'Moderate',
        emergency_contact: trip.emergency_contact || '',
        float_plan_filed: trip.float_plan_filed || false,
        float_plan_with: trip.float_plan_with || '',
        safety_equipment_check: trip.safety_equipment_check || false,
        notes: trip.notes || ''
      });
    }
  }, [trip]);

  const loadBoats = async () => {
    try {
      const response = await apiService.getBoats();
      setBoats(response.boats || []);
    } catch (err) {
      console.error('Failed to load boats:', err);
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
    setIsSubmitting(true);
    setError('');

    try {
      // Convert form data for API
      const processedData = { ...formData };
      
      // Convert empty strings to null for numeric fields
      const numericFields = [
        'planned_duration_hours', 'start_latitude', 'start_longitude', 
        'end_latitude', 'end_longitude'
      ];
      
      numericFields.forEach(field => {
        if (processedData[field] === '') {
          processedData[field] = null;
        } else if (processedData[field] !== null) {
          processedData[field] = parseFloat(processedData[field]) || null;
        }
      });

      // Convert boat_id to number
      if (processedData.boat_id) {
        processedData.boat_id = parseInt(processedData.boat_id);
      }

      // Handle dates - convert to ISO format
      if (processedData.start_date) {
        processedData.start_date = new Date(processedData.start_date).toISOString();
      }
      if (processedData.end_date) {
        processedData.end_date = new Date(processedData.end_date).toISOString();
      } else {
        processedData.end_date = null;
      }

      let result;
      if (trip) {
        result = await apiService.updateTrip(trip.id, processedData);
      } else {
        result = await apiService.createTrip(processedData);
      }

      onSave(result.trip);
    } catch (err) {
      setError(err.message || 'Failed to save trip');
    } finally {
      setIsSubmitting(false);
    }
  };

  const tripTypes = [
    'Leisure', 'Racing', 'Training', 'Delivery', 'Charter', 'Fishing', 'Maintenance', 'Other'
  ];

  const statusOptions = [
    'Planned', 'In Progress', 'Completed', 'Cancelled'
  ];

  const difficultyLevels = [
    'Easy', 'Moderate', 'Challenging', 'Expert'
  ];

  return (
    <div className="trip-form">
      <h3>{trip ? 'Edit Trip' : 'Plan New Trip'}</h3>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Basic Information */}
        <div className="form-section">
          <h4>Basic Information</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="name">Trip Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Weekend Cruise, Catalina Island Trip, etc."
              />
            </div>

            <div className="form-group">
              <label htmlFor="boat_id">Boat *</label>
              <select
                id="boat_id"
                name="boat_id"
                value={formData.boat_id}
                onChange={handleChange}
                required
              >
                <option value="">Select a Boat</option>
                {boats.map(boat => (
                  <option key={boat.id} value={boat.id}>{boat.name}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="trip_type">Trip Type</label>
              <select
                id="trip_type"
                name="trip_type"
                value={formData.trip_type}
                onChange={handleChange}
              >
                {tripTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleChange}
              >
                {statusOptions.map(status => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              placeholder="Brief description of the trip..."
            />
          </div>
        </div>

        {/* Timing */}
        <div className="form-section">
          <h4>Timing</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="start_date">Start Date & Time *</label>
              <input
                type="datetime-local"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_date">End Date & Time</label>
              <input
                type="datetime-local"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="planned_duration_hours">Planned Duration (hours)</label>
              <input
                type="number"
                id="planned_duration_hours"
                name="planned_duration_hours"
                value={formData.planned_duration_hours}
                onChange={handleChange}
                step="0.5"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="difficulty_level">Difficulty Level</label>
              <select
                id="difficulty_level"
                name="difficulty_level"
                value={formData.difficulty_level}
                onChange={handleChange}
              >
                {difficultyLevels.map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Locations */}
        <div className="form-section">
          <h4>Locations</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="start_location">Start Location</label>
              <input
                type="text"
                id="start_location"
                name="start_location"
                value={formData.start_location}
                onChange={handleChange}
                placeholder="Marina, harbor, or port name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_location">End Location</label>
              <input
                type="text"
                id="end_location"
                name="end_location"
                value={formData.end_location}
                onChange={handleChange}
                placeholder="Destination marina, harbor, or port"
              />
            </div>
          </div>

          <div className="form-subsection">
            <h5>GPS Coordinates (Optional)</h5>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="start_latitude">Start Latitude</label>
                <input
                  type="number"
                  id="start_latitude"
                  name="start_latitude"
                  value={formData.start_latitude}
                  onChange={handleChange}
                  step="0.0001"
                  min="-90"
                  max="90"
                  placeholder="34.0522"
                />
              </div>

              <div className="form-group">
                <label htmlFor="start_longitude">Start Longitude</label>
                <input
                  type="number"
                  id="start_longitude"
                  name="start_longitude"
                  value={formData.start_longitude}
                  onChange={handleChange}
                  step="0.0001"
                  min="-180"
                  max="180"
                  placeholder="-118.2437"
                />
              </div>

              <div className="form-group">
                <label htmlFor="end_latitude">End Latitude</label>
                <input
                  type="number"
                  id="end_latitude"
                  name="end_latitude"
                  value={formData.end_latitude}
                  onChange={handleChange}
                  step="0.0001"
                  min="-90"
                  max="90"
                  placeholder="33.3428"
                />
              </div>

              <div className="form-group">
                <label htmlFor="end_longitude">End Longitude</label>
                <input
                  type="number"
                  id="end_longitude"
                  name="end_longitude"
                  value={formData.end_longitude}
                  onChange={handleChange}
                  step="0.0001"
                  min="-180"
                  max="180"
                  placeholder="-118.3269"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Safety */}
        <div className="form-section">
          <h4>Safety & Planning</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="purpose">Purpose</label>
              <input
                type="text"
                id="purpose"
                name="purpose"
                value={formData.purpose}
                onChange={handleChange}
                placeholder="Pleasure, Business, Training, etc."
              />
            </div>

            <div className="form-group">
              <label htmlFor="emergency_contact">Emergency Contact</label>
              <input
                type="text"
                id="emergency_contact"
                name="emergency_contact"
                value={formData.emergency_contact}
                onChange={handleChange}
                placeholder="Name and phone number"
              />
            </div>

            <div className="form-group">
              <label htmlFor="float_plan_with">Float Plan Filed With</label>
              <input
                type="text"
                id="float_plan_with"
                name="float_plan_with"
                value={formData.float_plan_with}
                onChange={handleChange}
                placeholder="Harbormaster, friend, family member"
              />
            </div>
          </div>

          <div className="form-grid">
            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  name="float_plan_filed"
                  checked={formData.float_plan_filed}
                  onChange={handleChange}
                />
                Float plan filed
              </label>
            </div>

            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  name="safety_equipment_check"
                  checked={formData.safety_equipment_check}
                  onChange={handleChange}
                />
                Safety equipment checked
              </label>
            </div>
          </div>
        </div>

        {/* Notes */}
        <div className="form-section">
          <h4>Notes</h4>
          <div className="form-group">
            <label htmlFor="notes">Additional Notes</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows="4"
              placeholder="Weather conditions, special considerations, crew notes, etc."
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} disabled={isSubmitting}>
            Cancel
          </button>
          <button type="submit" disabled={isSubmitting || !formData.boat_id}>
            {isSubmitting ? 'Saving...' : (trip ? 'Update Trip' : 'Create Trip')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TripForm;