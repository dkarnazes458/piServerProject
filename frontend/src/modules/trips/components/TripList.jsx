import React, { useState } from 'react';

const TripList = ({ trips, onEdit, onDelete, onView }) => {
  const [sortField, setSortField] = useState('start_date');
  const [sortDirection, setSortDirection] = useState('desc');
  const [filter, setFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedTrips = trips
    .filter(trip => {
      const matchesSearch = trip.name.toLowerCase().includes(filter.toLowerCase()) ||
        (trip.start_location && trip.start_location.toLowerCase().includes(filter.toLowerCase())) ||
        (trip.end_location && trip.end_location.toLowerCase().includes(filter.toLowerCase())) ||
        (trip.boat_name && trip.boat_name.toLowerCase().includes(filter.toLowerCase()));
      
      const matchesStatus = !statusFilter || trip.status === statusFilter;
      
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      let aValue = a[sortField] || '';
      let bValue = b[sortField] || '';
      
      // Handle date sorting
      if (sortField === 'start_date' || sortField === 'end_date') {
        aValue = new Date(aValue || 0);
        bValue = new Date(bValue || 0);
      } else if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      if (sortDirection === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });

  const handleDelete = (trip) => {
    if (window.confirm(`Are you sure you want to delete "${trip.name}"?`)) {
      onDelete(trip);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString();
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

  const uniqueStatuses = [...new Set(trips.map(trip => trip.status).filter(Boolean))];

  return (
    <div className="trip-list">
      <div className="list-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search trips by name, location, or boat..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </div>
        <div className="filter-box">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Status</option>
            {uniqueStatuses.map(status => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </div>
      </div>

      {filteredAndSortedTrips.length === 0 ? (
        <div className="empty-state">
          {trips.length === 0 ? (
            <p>No trips logged yet. Click "Plan Trip" to get started.</p>
          ) : (
            <p>No trips match your search criteria.</p>
          )}
        </div>
      ) : (
        <div className="trips-table-container">
          <table className="trips-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('name')} className="sortable">
                  Trip Name {sortField === 'name' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('boat_name')} className="sortable">
                  Boat {sortField === 'boat_name' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('start_date')} className="sortable">
                  Start Date {sortField === 'start_date' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('end_date')} className="sortable">
                  End Date {sortField === 'end_date' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>Route</th>
                <th onClick={() => handleSort('status')} className="sortable">
                  Status {sortField === 'status' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAndSortedTrips.map(trip => (
                <tr key={trip.id}>
                  <td>
                    <strong>{trip.name}</strong>
                    {trip.trip_type && (
                      <div className="trip-type">{trip.trip_type}</div>
                    )}
                  </td>
                  <td>{trip.boat_name || '-'}</td>
                  <td>
                    {formatDate(trip.start_date)}
                    {trip.start_date && (
                      <div className="trip-time">
                        {new Date(trip.start_date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </div>
                    )}
                  </td>
                  <td>
                    {formatDate(trip.end_date)}
                    {trip.end_date && (
                      <div className="trip-time">
                        {new Date(trip.end_date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </div>
                    )}
                  </td>
                  <td>
                    <div className="route-info">
                      {trip.start_location && (
                        <div className="route-start">From: {trip.start_location}</div>
                      )}
                      {trip.end_location && (
                        <div className="route-end">To: {trip.end_location}</div>
                      )}
                      {!trip.start_location && !trip.end_location && '-'}
                    </div>
                  </td>
                  <td>
                    <span className={`status-badge ${getStatusClass(trip.status)}`}>
                      {trip.status}
                    </span>
                    {trip.difficulty_level && (
                      <div className="difficulty">Difficulty: {trip.difficulty_level}</div>
                    )}
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        onClick={() => onView(trip)}
                        className="btn-view"
                        title="View Details"
                      >
                        👁️
                      </button>
                      <button 
                        onClick={() => onEdit(trip)}
                        className="btn-edit"
                        title="Edit Trip"
                      >
                        ✏️
                      </button>
                      <button 
                        onClick={() => handleDelete(trip)}
                        className="btn-delete"
                        title="Delete Trip"
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TripList;