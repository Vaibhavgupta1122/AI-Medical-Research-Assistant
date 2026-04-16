import React, { useState } from 'react';
import './ContextPanel.css';

function ContextPanel({ context, onUpdate, onClose }) {
  const [localContext, setLocalContext] = useState({
    primaryCondition: '',
    secondaryConditions: '',
    symptoms: '',
    medications: '',
    age: '',
    gender: '',
    location: {
      country: '',
      state: '',
      city: ''
    },
    ...context
  });

  const handleInputChange = (field, value) => {
    setLocalContext(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleLocationChange = (field, value) => {
    setLocalContext(prev => ({
      ...prev,
      location: {
        ...prev.location,
        [field]: value
      }
    }));
  };

  const handleApply = () => {
    // Clean up empty values
    const cleanedContext = {
      primaryCondition: localContext.primaryCondition.trim(),
      secondaryConditions: localContext.secondaryConditions
        .split(',')
        .map(s => s.trim())
        .filter(s => s),
      symptoms: localContext.symptoms
        .split(',')
        .map(s => s.trim())
        .filter(s => s),
      medications: localContext.medications
        .split(',')
        .map(s => s.trim())
        .filter(s => s),
      age: localContext.age ? parseInt(localContext.age) : undefined,
      gender: localContext.gender || undefined,
      location: {
        country: localContext.location.country.trim(),
        state: localContext.location.state.trim(),
        city: localContext.location.city.trim()
      }
    };

    onUpdate(cleanedContext);
    onClose();
  };

  const handleClear = () => {
    setLocalContext({
      primaryCondition: '',
      secondaryConditions: '',
      symptoms: '',
      medications: '',
      age: '',
      gender: '',
      location: { country: '', state: '', city: '' }
    });
  };

  return (
    <div className="context-panel">
      <div className="context-header">
        <h3>Medical Context</h3>
        <button className="close-button" onClick={onClose}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div className="context-content">
        <div className="context-section">
          <h4>Primary Condition</h4>
          <input
            type="text"
            value={localContext.primaryCondition}
            onChange={(e) => handleInputChange('primaryCondition', e.target.value)}
            placeholder="e.g., Parkinson disease"
            className="context-input"
          />
        </div>

        <div className="context-section">
          <h4>Secondary Conditions</h4>
          <input
            type="text"
            value={localContext.secondaryConditions}
            onChange={(e) => handleInputChange('secondaryConditions', e.target.value)}
            placeholder="e.g., Diabetes, Hypertension (comma-separated)"
            className="context-input"
          />
        </div>

        <div className="context-section">
          <h4>Current Symptoms</h4>
          <input
            type="text"
            value={localContext.symptoms}
            onChange={(e) => handleInputChange('symptoms', e.target.value)}
            placeholder="e.g., Tremors, Memory loss (comma-separated)"
            className="context-input"
          />
        </div>

        <div className="context-section">
          <h4>Current Medications</h4>
          <input
            type="text"
            value={localContext.medications}
            onChange={(e) => handleInputChange('medications', e.target.value)}
            placeholder="e.g., Levodopa, Metformin (comma-separated)"
            className="context-input"
          />
        </div>

        <div className="context-row">
          <div className="context-section half-width">
            <h4>Age</h4>
            <input
              type="number"
              value={localContext.age}
              onChange={(e) => handleInputChange('age', e.target.value)}
              placeholder="e.g., 65"
              className="context-input"
              min="1"
              max="120"
            />
          </div>

          <div className="context-section half-width">
            <h4>Gender</h4>
            <select
              value={localContext.gender}
              onChange={(e) => handleInputChange('gender', e.target.value)}
              className="context-select"
            >
              <option value="">Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="prefer_not_to_say">Prefer not to say</option>
            </select>
          </div>
        </div>

        <div className="context-section">
          <h4>Location (for clinical trials)</h4>
          <div className="location-inputs">
            <input
              type="text"
              value={localContext.location.country}
              onChange={(e) => handleLocationChange('country', e.target.value)}
              placeholder="Country"
              className="context-input location-input"
            />
            <input
              type="text"
              value={localContext.location.state}
              onChange={(e) => handleLocationChange('state', e.target.value)}
              placeholder="State/Province"
              className="context-input location-input"
            />
            <input
              type="text"
              value={localContext.location.city}
              onChange={(e) => handleLocationChange('city', e.target.value)}
              placeholder="City"
              className="context-input location-input"
            />
          </div>
        </div>
      </div>

      <div className="context-footer">
        <div className="context-info">
          <p>
            Providing context helps me find more relevant research and clinical trials for you.
          </p>
        </div>
        <div className="context-actions">
          <button className="btn btn-secondary" onClick={handleClear}>
            Clear
          </button>
          <button className="btn btn-primary" onClick={handleApply}>
            Apply Context
          </button>
        </div>
      </div>
    </div>
  );
}

export default ContextPanel;
