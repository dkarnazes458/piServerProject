import React, { useState, useEffect } from 'react';
import apiService from '../../../services/api';

const BoatForm = ({ boat = null, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    boat_type: '',
    length_feet: '',
    beam_feet: '',
    draft_feet: '',
    displacement_lbs: '',
    year_built: '',
    hull_material: '',
    registration_number: '',
    hin: '',
    documentation_number: '',
    home_port: '',
    current_location: '',
    marina_berth: '',
    insurance_company: '',
    insurance_policy_number: '',
    insurance_expiry: '',
    engine_make: '',
    engine_model: '',
    engine_year: '',
    engine_hours: '',
    fuel_capacity_gallons: '',
    water_capacity_gallons: '',
    sail_area_sqft: '',
    mast_height_feet: '',
    keel_type: '',
    condition: 'Good',
    last_survey_date: '',
    next_survey_due: '',
    notes: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (boat) {
      setFormData({
        name: boat.name || '',
        boat_type: boat.boat_type || '',
        length_feet: boat.length_feet || '',
        beam_feet: boat.beam_feet || '',
        draft_feet: boat.draft_feet || '',
        displacement_lbs: boat.displacement_lbs || '',
        year_built: boat.year_built || '',
        hull_material: boat.hull_material || '',
        registration_number: boat.registration_number || '',
        hin: boat.hin || '',
        documentation_number: boat.documentation_number || '',
        home_port: boat.home_port || '',
        current_location: boat.current_location || '',
        marina_berth: boat.marina_berth || '',
        insurance_company: boat.insurance_company || '',
        insurance_policy_number: boat.insurance_policy_number || '',
        insurance_expiry: boat.insurance_expiry || '',
        engine_make: boat.engine_make || '',
        engine_model: boat.engine_model || '',
        engine_year: boat.engine_year || '',
        engine_hours: boat.engine_hours || '',
        fuel_capacity_gallons: boat.fuel_capacity_gallons || '',
        water_capacity_gallons: boat.water_capacity_gallons || '',
        sail_area_sqft: boat.sail_area_sqft || '',
        mast_height_feet: boat.mast_height_feet || '',
        keel_type: boat.keel_type || '',
        condition: boat.condition || 'Good',
        last_survey_date: boat.last_survey_date || '',
        next_survey_due: boat.next_survey_due || '',
        notes: boat.notes || ''
      });
    }
  }, [boat]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      // Convert empty strings to null for numeric fields
      const processedData = { ...formData };
      const numericFields = [
        'length_feet', 'beam_feet', 'draft_feet', 'displacement_lbs', 'year_built',
        'engine_year', 'engine_hours', 'fuel_capacity_gallons', 'water_capacity_gallons',
        'sail_area_sqft', 'mast_height_feet'
      ];
      
      numericFields.forEach(field => {
        if (processedData[field] === '') {
          processedData[field] = null;
        } else if (processedData[field] !== null) {
          processedData[field] = parseFloat(processedData[field]) || null;
        }
      });

      // Handle date fields
      ['insurance_expiry', 'last_survey_date', 'next_survey_due'].forEach(field => {
        if (processedData[field] === '') {
          processedData[field] = null;
        }
      });

      let result;
      if (boat) {
        result = await apiService.updateBoat(boat.id, processedData);
      } else {
        result = await apiService.createBoat(processedData);
      }

      onSave(result.boat);
    } catch (err) {
      setError(err.message || 'Failed to save boat');
    } finally {
      setIsSubmitting(false);
    }
  };

  const boatTypes = [
    'Sailboat', 'Motorboat', 'Catamaran', 'Trimaran', 'Yacht', 'Dinghy', 
    'Powerboat', 'Fishing Boat', 'Other'
  ];

  const hullMaterials = [
    'Fiberglass', 'Wood', 'Steel', 'Aluminum', 'Carbon Fiber', 'Composite', 'Other'
  ];

  const keelTypes = [
    'Full', 'Fin', 'Wing', 'Centerboard', 'Daggerboard', 'Bulb', 'Other'
  ];

  const conditions = ['Excellent', 'Good', 'Fair', 'Poor'];

  return (
    <div className="boat-form">
      <h3>{boat ? 'Edit Boat' : 'Add New Boat'}</h3>
      
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
              <label htmlFor="name">Boat Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="boat_type">Boat Type</label>
              <select
                id="boat_type"
                name="boat_type"
                value={formData.boat_type}
                onChange={handleChange}
              >
                <option value="">Select Type</option>
                {boatTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="year_built">Year Built</label>
              <input
                type="number"
                id="year_built"
                name="year_built"
                value={formData.year_built}
                onChange={handleChange}
                min="1800"
                max={new Date().getFullYear()}
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

        {/* Dimensions */}
        <div className="form-section">
          <h4>Dimensions</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="length_feet">Length (feet)</label>
              <input
                type="number"
                id="length_feet"
                name="length_feet"
                value={formData.length_feet}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="beam_feet">Beam (feet)</label>
              <input
                type="number"
                id="beam_feet"
                name="beam_feet"
                value={formData.beam_feet}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="draft_feet">Draft (feet)</label>
              <input
                type="number"
                id="draft_feet"
                name="draft_feet"
                value={formData.draft_feet}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="displacement_lbs">Displacement (lbs)</label>
              <input
                type="number"
                id="displacement_lbs"
                name="displacement_lbs"
                value={formData.displacement_lbs}
                onChange={handleChange}
                min="0"
              />
            </div>
          </div>
        </div>

        {/* Construction */}
        <div className="form-section">
          <h4>Construction</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="hull_material">Hull Material</label>
              <select
                id="hull_material"
                name="hull_material"
                value={formData.hull_material}
                onChange={handleChange}
              >
                <option value="">Select Material</option>
                {hullMaterials.map(material => (
                  <option key={material} value={material}>{material}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="keel_type">Keel Type</label>
              <select
                id="keel_type"
                name="keel_type"
                value={formData.keel_type}
                onChange={handleChange}
              >
                <option value="">Select Keel Type</option>
                {keelTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Registration */}
        <div className="form-section">
          <h4>Registration & Documentation</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="registration_number">Registration Number</label>
              <input
                type="text"
                id="registration_number"
                name="registration_number"
                value={formData.registration_number}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="hin">Hull ID Number (HIN)</label>
              <input
                type="text"
                id="hin"
                name="hin"
                value={formData.hin}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="documentation_number">Documentation Number</label>
              <input
                type="text"
                id="documentation_number"
                name="documentation_number"
                value={formData.documentation_number}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        {/* Location */}
        <div className="form-section">
          <h4>Location</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="home_port">Home Port</label>
              <input
                type="text"
                id="home_port"
                name="home_port"
                value={formData.home_port}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="current_location">Current Location</label>
              <input
                type="text"
                id="current_location"
                name="current_location"
                value={formData.current_location}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="marina_berth">Marina/Berth</label>
              <input
                type="text"
                id="marina_berth"
                name="marina_berth"
                value={formData.marina_berth}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        {/* Engine */}
        <div className="form-section">
          <h4>Engine</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="engine_make">Engine Make</label>
              <input
                type="text"
                id="engine_make"
                name="engine_make"
                value={formData.engine_make}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="engine_model">Engine Model</label>
              <input
                type="text"
                id="engine_model"
                name="engine_model"
                value={formData.engine_model}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="engine_year">Engine Year</label>
              <input
                type="number"
                id="engine_year"
                name="engine_year"
                value={formData.engine_year}
                onChange={handleChange}
                min="1900"
                max={new Date().getFullYear()}
              />
            </div>

            <div className="form-group">
              <label htmlFor="engine_hours">Engine Hours</label>
              <input
                type="number"
                id="engine_hours"
                name="engine_hours"
                value={formData.engine_hours}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>
          </div>
        </div>

        {/* Capacities */}
        <div className="form-section">
          <h4>Capacities</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="fuel_capacity_gallons">Fuel Capacity (gallons)</label>
              <input
                type="number"
                id="fuel_capacity_gallons"
                name="fuel_capacity_gallons"
                value={formData.fuel_capacity_gallons}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="water_capacity_gallons">Water Capacity (gallons)</label>
              <input
                type="number"
                id="water_capacity_gallons"
                name="water_capacity_gallons"
                value={formData.water_capacity_gallons}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>
          </div>
        </div>

        {/* Sailing Specs */}
        <div className="form-section">
          <h4>Sailing Specifications</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="sail_area_sqft">Sail Area (sq ft)</label>
              <input
                type="number"
                id="sail_area_sqft"
                name="sail_area_sqft"
                value={formData.sail_area_sqft}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="mast_height_feet">Mast Height (feet)</label>
              <input
                type="number"
                id="mast_height_feet"
                name="mast_height_feet"
                value={formData.mast_height_feet}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>
          </div>
        </div>

        {/* Insurance */}
        <div className="form-section">
          <h4>Insurance</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="insurance_company">Insurance Company</label>
              <input
                type="text"
                id="insurance_company"
                name="insurance_company"
                value={formData.insurance_company}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="insurance_policy_number">Policy Number</label>
              <input
                type="text"
                id="insurance_policy_number"
                name="insurance_policy_number"
                value={formData.insurance_policy_number}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="insurance_expiry">Insurance Expiry</label>
              <input
                type="date"
                id="insurance_expiry"
                name="insurance_expiry"
                value={formData.insurance_expiry}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        {/* Survey */}
        <div className="form-section">
          <h4>Survey Information</h4>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="last_survey_date">Last Survey Date</label>
              <input
                type="date"
                id="last_survey_date"
                name="last_survey_date"
                value={formData.last_survey_date}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="next_survey_due">Next Survey Due</label>
              <input
                type="date"
                id="next_survey_due"
                name="next_survey_due"
                value={formData.next_survey_due}
                onChange={handleChange}
              />
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
              placeholder="Any additional information about the boat..."
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} disabled={isSubmitting}>
            Cancel
          </button>
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : (boat ? 'Update Boat' : 'Create Boat')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BoatForm;