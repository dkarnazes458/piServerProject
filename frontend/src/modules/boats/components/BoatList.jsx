import React, { useState } from 'react';

const BoatList = ({ boats, onEdit, onDelete, onView }) => {
  const [sortField, setSortField] = useState('name');
  const [sortDirection, setSortDirection] = useState('asc');
  const [filter, setFilter] = useState('');

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedBoats = boats
    .filter(boat => 
      boat.name.toLowerCase().includes(filter.toLowerCase()) ||
      (boat.boat_type && boat.boat_type.toLowerCase().includes(filter.toLowerCase())) ||
      (boat.home_port && boat.home_port.toLowerCase().includes(filter.toLowerCase()))
    )
    .sort((a, b) => {
      let aValue = a[sortField] || '';
      let bValue = b[sortField] || '';
      
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      if (sortDirection === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });

  const handleDelete = (boat) => {
    if (window.confirm(`Are you sure you want to delete "${boat.name}"?`)) {
      onDelete(boat);
    }
  };

  return (
    <div className="boat-list">
      <div className="list-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search boats by name, type, or port..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </div>
      </div>

      {filteredAndSortedBoats.length === 0 ? (
        <div className="empty-state">
          {boats.length === 0 ? (
            <p>No boats registered yet. Click "Add Boat" to get started.</p>
          ) : (
            <p>No boats match your search criteria.</p>
          )}
        </div>
      ) : (
        <div className="boats-table-container">
          <table className="boats-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('name')} className="sortable">
                  Name {sortField === 'name' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('boat_type')} className="sortable">
                  Type {sortField === 'boat_type' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('length_feet')} className="sortable">
                  Length {sortField === 'length_feet' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('year_built')} className="sortable">
                  Year {sortField === 'year_built' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('home_port')} className="sortable">
                  Home Port {sortField === 'home_port' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('condition')} className="sortable">
                  Condition {sortField === 'condition' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAndSortedBoats.map(boat => (
                <tr key={boat.id}>
                  <td>
                    <strong>{boat.name}</strong>
                    {boat.registration_number && (
                      <div className="boat-reg">Reg: {boat.registration_number}</div>
                    )}
                  </td>
                  <td>{boat.boat_type || '-'}</td>
                  <td>
                    {boat.length_feet ? `${boat.length_feet}'` : '-'}
                    {boat.beam_feet && (
                      <div className="boat-beam">Beam: {boat.beam_feet}'</div>
                    )}
                  </td>
                  <td>
                    {boat.year_built || '-'}
                    {boat.age_years !== null && (
                      <div className="boat-age">({boat.age_years} years)</div>
                    )}
                  </td>
                  <td>{boat.home_port || '-'}</td>
                  <td>
                    <span className={`condition-badge condition-${boat.condition?.toLowerCase()}`}>
                      {boat.condition}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        onClick={() => onView(boat)}
                        className="btn-view"
                        title="View Details"
                      >
                        👁️
                      </button>
                      <button 
                        onClick={() => onEdit(boat)}
                        className="btn-edit"
                        title="Edit Boat"
                      >
                        ✏️
                      </button>
                      <button 
                        onClick={() => handleDelete(boat)}
                        className="btn-delete"
                        title="Delete Boat"
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

export default BoatList;