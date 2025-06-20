import React from 'react';

const BoatDetail = ({ boat, onEdit, onClose }) => {
  if (!boat) return null;

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString();
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined) return '-';
    return typeof num === 'number' ? num.toLocaleString() : num;
  };

  return (
    <div className="boat-detail">
      <div className="detail-header">
        <h3>{boat.name}</h3>
        <div className="header-actions">
          <button onClick={() => onEdit(boat)} className="btn-edit">
            Edit Boat
          </button>
          <button onClick={onClose} className="btn-close">
            ✕
          </button>
        </div>
      </div>

      <div className="detail-content">
        <div className="detail-grid">
          {/* Basic Information */}
          <div className="detail-section">
            <h4>Basic Information</h4>
            <div className="detail-item">
              <label>Name:</label>
              <span>{boat.name}</span>
            </div>
            <div className="detail-item">
              <label>Type:</label>
              <span>{boat.boat_type || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Year Built:</label>
              <span>
                {boat.year_built || '-'}
                {boat.age_years !== null && ` (${boat.age_years} years old)`}
              </span>
            </div>
            <div className="detail-item">
              <label>Condition:</label>
              <span className={`condition-badge condition-${boat.condition?.toLowerCase()}`}>
                {boat.condition}
              </span>
            </div>
          </div>

          {/* Dimensions */}
          <div className="detail-section">
            <h4>Dimensions</h4>
            <div className="detail-item">
              <label>Length:</label>
              <span>{boat.length_feet ? `${boat.length_feet} feet` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Beam:</label>
              <span>{boat.beam_feet ? `${boat.beam_feet} feet` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Draft:</label>
              <span>{boat.draft_feet ? `${boat.draft_feet} feet` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Displacement:</label>
              <span>{boat.displacement_lbs ? `${formatNumber(boat.displacement_lbs)} lbs` : '-'}</span>
            </div>
          </div>

          {/* Construction */}
          <div className="detail-section">
            <h4>Construction</h4>
            <div className="detail-item">
              <label>Hull Material:</label>
              <span>{boat.hull_material || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Keel Type:</label>
              <span>{boat.keel_type || '-'}</span>
            </div>
          </div>

          {/* Registration */}
          <div className="detail-section">
            <h4>Registration & Documentation</h4>
            <div className="detail-item">
              <label>Registration Number:</label>
              <span>{boat.registration_number || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Hull ID Number:</label>
              <span>{boat.hin || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Documentation Number:</label>
              <span>{boat.documentation_number || '-'}</span>
            </div>
          </div>

          {/* Location */}
          <div className="detail-section">
            <h4>Location</h4>
            <div className="detail-item">
              <label>Home Port:</label>
              <span>{boat.home_port || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Current Location:</label>
              <span>{boat.current_location || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Marina/Berth:</label>
              <span>{boat.marina_berth || '-'}</span>
            </div>
          </div>

          {/* Engine */}
          <div className="detail-section">
            <h4>Engine</h4>
            <div className="detail-item">
              <label>Make & Model:</label>
              <span>
                {boat.engine_make && boat.engine_model 
                  ? `${boat.engine_make} ${boat.engine_model}`
                  : boat.engine_make || boat.engine_model || '-'
                }
              </span>
            </div>
            <div className="detail-item">
              <label>Year:</label>
              <span>{boat.engine_year || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Hours:</label>
              <span>{boat.engine_hours ? `${formatNumber(boat.engine_hours)} hrs` : '-'}</span>
            </div>
          </div>

          {/* Capacities */}
          <div className="detail-section">
            <h4>Capacities</h4>
            <div className="detail-item">
              <label>Fuel:</label>
              <span>{boat.fuel_capacity_gallons ? `${boat.fuel_capacity_gallons} gallons` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Water:</label>
              <span>{boat.water_capacity_gallons ? `${boat.water_capacity_gallons} gallons` : '-'}</span>
            </div>
          </div>

          {/* Sailing Specs */}
          <div className="detail-section">
            <h4>Sailing Specifications</h4>
            <div className="detail-item">
              <label>Sail Area:</label>
              <span>{boat.sail_area_sqft ? `${formatNumber(boat.sail_area_sqft)} sq ft` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Mast Height:</label>
              <span>{boat.mast_height_feet ? `${boat.mast_height_feet} feet` : '-'}</span>
            </div>
          </div>

          {/* Insurance */}
          <div className="detail-section">
            <h4>Insurance</h4>
            <div className="detail-item">
              <label>Company:</label>
              <span>{boat.insurance_company || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Policy Number:</label>
              <span>{boat.insurance_policy_number || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Expiry Date:</label>
              <span>{formatDate(boat.insurance_expiry)}</span>
            </div>
          </div>

          {/* Survey */}
          <div className="detail-section">
            <h4>Survey Information</h4>
            <div className="detail-item">
              <label>Last Survey:</label>
              <span>{formatDate(boat.last_survey_date)}</span>
            </div>
            <div className="detail-item">
              <label>Next Survey Due:</label>
              <span>{formatDate(boat.next_survey_due)}</span>
            </div>
          </div>

          {/* Notes */}
          {boat.notes && (
            <div className="detail-section full-width">
              <h4>Notes</h4>
              <div className="detail-notes">
                {boat.notes}
              </div>
            </div>
          )}

          {/* Timestamps */}
          <div className="detail-section">
            <h4>Record Information</h4>
            <div className="detail-item">
              <label>Created:</label>
              <span>{formatDate(boat.created_at)}</span>
            </div>
            <div className="detail-item">
              <label>Last Updated:</label>
              <span>{formatDate(boat.updated_at)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BoatDetail;