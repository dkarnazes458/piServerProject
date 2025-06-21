/**
 * Equipment Module
 * 
 * Equipment inventory and tracking
 */
import React, { useState } from 'react';
import EquipmentList from './components/EquipmentList';
import EquipmentForm from './components/EquipmentForm';
import EquipmentDetail from './components/EquipmentDetail';
import '../shared.css';
import './equipment.css';

const EquipmentModule = ({ user }) => {
  const [currentView, setCurrentView] = useState('list');
  const [selectedEquipment, setSelectedEquipment] = useState(null);

  const handleSelectEquipment = (equipment) => {
    setSelectedEquipment(equipment);
    setCurrentView('detail');
  };

  const handleEditEquipment = (equipment) => {
    setSelectedEquipment(equipment);
    setCurrentView('form');
  };

  const handleAddEquipment = () => {
    setSelectedEquipment(null);
    setCurrentView('form');
  };

  const handleSaveEquipment = (equipment) => {
    setSelectedEquipment(equipment);
    setCurrentView('detail');
  };

  const handleCancel = () => {
    setSelectedEquipment(null);
    setCurrentView('list');
  };

  const handleBackToList = () => {
    setSelectedEquipment(null);
    setCurrentView('list');
  };

  const handleDeleteEquipment = () => {
    setSelectedEquipment(null);
    setCurrentView('list');
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'form':
        return (
          <EquipmentForm
            equipment={selectedEquipment}
            onSave={handleSaveEquipment}
            onCancel={handleCancel}
          />
        );
      case 'detail':
        return (
          <EquipmentDetail
            equipment={selectedEquipment}
            onEdit={handleEditEquipment}
            onBack={handleBackToList}
            onDelete={handleDeleteEquipment}
          />
        );
      case 'list':
      default:
        return (
          <EquipmentList
            onSelect={handleSelectEquipment}
            onEdit={handleEditEquipment}
            onAdd={handleAddEquipment}
          />
        );
    }
  };

  return (
    <div className="module-container">
      {renderCurrentView()}
    </div>
  );
};

export default EquipmentModule;