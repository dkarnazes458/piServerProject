import React from 'react';

const TripDetail = ({ trip, onEdit, onClose }) => {
  if (!trip) return null;

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString();
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleString();
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined) return '-';
    return typeof num === 'number' ? num.toLocaleString() : num;
  };

  const formatDuration = (hours) => {
    if (!hours) return '-';
    const wholeHours = Math.floor(hours);
    const minutes = Math.round((hours - wholeHours) * 60);
    if (wholeHours === 0) return `${minutes}m`;
    if (minutes === 0) return `${wholeHours}h`;
    return `${wholeHours}h ${minutes}m`;
  };

  const getStatusClass = (status) => {
    switch (status?.toLowerCase()) {
      case 'planned': return 'status-planned';
      case 'in progress': return 'status-in-progress';
      case 'completed': return 'status-completed';
      case 'cancelled': return 'status-cancelled';
      default: return 'status-unknown';
    }
  };

  const formatCoordinate = (lat, lng) => {
    if (!lat || !lng) return '-';
    return `${lat}, ${lng}`;
  };

  return (
    <div className="trip-detail">
      <div className="detail-header">
        <h3>{trip.name}</h3>
        <div className="header-actions">
          <button onClick={() => onEdit(trip)} className="btn-edit">
            Edit Trip
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
              <label>Trip Name:</label>
              <span>{trip.name}</span>
            </div>
            <div className="detail-item">
              <label>Type:</label>
              <span>{trip.trip_type || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Boat:</label>
              <span>{trip.boat_name || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Captain:</label>
              <span>{trip.captain_name || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Status:</label>
              <span className={`status-badge ${getStatusClass(trip.status)}`}>
                {trip.status}
              </span>
            </div>
            <div className="detail-item">
              <label>Difficulty:</label>
              <span>{trip.difficulty_level || '-'}</span>
            </div>
          </div>

          {/* Timing */}
          <div className="detail-section">
            <h4>Timing</h4>
            <div className="detail-item">
              <label>Start Date & Time:</label>
              <span>{formatDateTime(trip.start_date)}</span>
            </div>
            <div className="detail-item">
              <label>End Date & Time:</label>
              <span>{formatDateTime(trip.end_date)}</span>
            </div>
            <div className="detail-item">
              <label>Planned Duration:</label>
              <span>{formatDuration(trip.planned_duration_hours)}</span>
            </div>
            <div className="detail-item">
              <label>Actual Duration:</label>
              <span>{formatDuration(trip.actual_duration_hours)}</span>
            </div>
            {trip.days_since_trip !== null && trip.days_since_trip >= 0 && (
              <div className="detail-item">
                <label>Days Since Trip:</label>
                <span>{trip.days_since_trip} days ago</span>
              </div>
            )}
          </div>

          {/* Locations */}
          <div className="detail-section">
            <h4>Locations</h4>
            <div className="detail-item">
              <label>Start Location:</label>
              <span>{trip.start_location || '-'}</span>
            </div>
            <div className="detail-item">
              <label>End Location:</label>
              <span>{trip.end_location || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Start Coordinates:</label>
              <span>{formatCoordinate(trip.start_latitude, trip.start_longitude)}</span>
            </div>
            <div className="detail-item">
              <label>End Coordinates:</label>
              <span>{formatCoordinate(trip.end_latitude, trip.end_longitude)}</span>
            </div>
          </div>

          {/* Trip Metrics */}
          <div className="detail-section">
            <h4>Trip Metrics</h4>
            <div className="detail-item">
              <label>Distance:</label>
              <span>{trip.distance_miles ? `${trip.distance_miles} nautical miles` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Average Speed:</label>
              <span>{trip.avg_speed_knots ? `${trip.avg_speed_knots} knots` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Max Speed:</label>
              <span>{trip.max_speed_knots ? `${trip.max_speed_knots} knots` : '-'}</span>
            </div>
            <div className="detail-item">
              <label>Crew Size:</label>
              <span>{trip.crew_size || '-'}</span>
            </div>
          </div>

          {/* Weather & Conditions */}
          {(trip.weather_conditions || trip.sea_conditions || trip.visibility || 
            trip.max_wind_speed_knots || trip.avg_wind_speed_knots || trip.wind_direction) && (
            <div className="detail-section">
              <h4>Weather & Conditions</h4>
              {trip.max_wind_speed_knots && (
                <div className="detail-item">
                  <label>Max Wind Speed:</label>
                  <span>{trip.max_wind_speed_knots} knots</span>
                </div>
              )}
              {trip.avg_wind_speed_knots && (
                <div className="detail-item">
                  <label>Avg Wind Speed:</label>
                  <span>{trip.avg_wind_speed_knots} knots</span>
                </div>
              )}
              {trip.wind_direction && (
                <div className="detail-item">
                  <label>Wind Direction:</label>
                  <span>{trip.wind_direction}</span>
                </div>
              )}
              {trip.visibility && (
                <div className="detail-item">
                  <label>Visibility:</label>
                  <span>{trip.visibility}</span>
                </div>
              )}
              {trip.sea_conditions && (
                <div className="detail-item">
                  <label>Sea Conditions:</label>
                  <span>{trip.sea_conditions}</span>
                </div>
              )}
            </div>
          )}

          {/* Safety & Planning */}
          <div className="detail-section">
            <h4>Safety & Planning</h4>
            <div className="detail-item">
              <label>Purpose:</label>
              <span>{trip.purpose || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Emergency Contact:</label>
              <span>{trip.emergency_contact || '-'}</span>
            </div>
            <div className="detail-item">
              <label>Float Plan Filed:</label>
              <span>{trip.float_plan_filed ? 'Yes' : 'No'}</span>
            </div>
            {trip.float_plan_with && (
              <div className="detail-item">
                <label>Float Plan With:</label>
                <span>{trip.float_plan_with}</span>
              </div>
            )}
            <div className="detail-item">
              <label>Safety Equipment Checked:</label>
              <span>{trip.safety_equipment_check ? 'Yes' : 'No'}</span>
            </div>
          </div>

          {/* Fuel & Costs */}
          {(trip.fuel_used_gallons || trip.fuel_cost || trip.total_cost) && (
            <div className="detail-section">
              <h4>Fuel & Costs</h4>
              {trip.fuel_used_gallons && (
                <div className="detail-item">
                  <label>Fuel Used:</label>
                  <span>{trip.fuel_used_gallons} gallons</span>
                </div>
              )}
              {trip.fuel_cost && (
                <div className="detail-item">
                  <label>Fuel Cost:</label>
                  <span>${trip.fuel_cost}</span>
                </div>
              )}
              {trip.total_cost && (
                <div className="detail-item">
                  <label>Total Cost:</label>
                  <span>${trip.total_cost}</span>
                </div>
              )}
            </div>
          )}

          {/* GPS & Route Data */}
          {(trip.gps_file_name || trip.total_route_points) && (
            <div className="detail-section">
              <h4>GPS & Route Data</h4>
              {trip.gps_file_name && (
                <div className="detail-item">
                  <label>GPS File:</label>
                  <span>{trip.gps_file_name}</span>
                </div>
              )}
              {trip.total_route_points && (
                <div className="detail-item">
                  <label>Route Points:</label>
                  <span>{formatNumber(trip.total_route_points)}</span>
                </div>
              )}
              <div className="detail-item">
                <label>Route Processed:</label>
                <span>{trip.route_processed ? 'Yes' : 'No'}</span>
              </div>
            </div>
          )}

          {/* Experience & Learning */}
          {(trip.overall_rating || trip.highlights || trip.challenges_faced || 
            trip.lessons_learned || trip.would_repeat !== null) && (
            <div className="detail-section">
              <h4>Experience & Learning</h4>
              {trip.overall_rating && (
                <div className="detail-item">
                  <label>Overall Rating:</label>
                  <span>{'⭐'.repeat(trip.overall_rating)} ({trip.overall_rating}/5)</span>
                </div>
              )}
              {trip.would_repeat !== null && (
                <div className="detail-item">
                  <label>Would Repeat:</label>
                  <span>{trip.would_repeat ? 'Yes' : 'No'}</span>
                </div>
              )}
              {trip.highlights && (
                <div className="detail-item">
                  <label>Highlights:</label>
                  <span>{trip.highlights}</span>
                </div>
              )}
              {trip.challenges_faced && (
                <div className="detail-item">
                  <label>Challenges:</label>
                  <span>{trip.challenges_faced}</span>
                </div>
              )}
              {trip.lessons_learned && (
                <div className="detail-item">
                  <label>Lessons Learned:</label>
                  <span>{trip.lessons_learned}</span>
                </div>
              )}
            </div>
          )}

          {/* Description/Notes */}
          {(trip.description || trip.notes) && (
            <div className="detail-section full-width">
              <h4>Notes & Description</h4>
              {trip.description && (
                <div className="detail-notes">
                  <h5>Description:</h5>
                  <div>{trip.description}</div>
                </div>
              )}
              {trip.notes && (
                <div className="detail-notes">
                  <h5>Additional Notes:</h5>
                  <div>{trip.notes}</div>
                </div>
              )}
            </div>
          )}

          {/* Trip Settings */}
          <div className="detail-section">
            <h4>Trip Settings</h4>
            <div className="detail-item">
              <label>Public Trip:</label>
              <span>{trip.is_public ? 'Yes' : 'No'}</span>
            </div>
            <div className="detail-item">
              <label>Favorite Trip:</label>
              <span>{trip.is_favorite ? 'Yes' : 'No'}</span>
            </div>
          </div>

          {/* Record Information */}
          <div className="detail-section">
            <h4>Record Information</h4>
            <div className="detail-item">
              <label>Created:</label>
              <span>{formatDateTime(trip.created_at)}</span>
            </div>
            <div className="detail-item">
              <label>Last Updated:</label>
              <span>{formatDateTime(trip.updated_at)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripDetail;