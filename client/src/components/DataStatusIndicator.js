import React from 'react';
import './DataStatusIndicator.css';

const DataStatusIndicator = ({ status, message }) => {
    const getStatusIcon = () => {
        switch (status) {
            case 'loading':
                return (
                    <div className="status-icon loading">
                        <div className="spinner"></div>
                    </div>
                );
            case 'success':
                return (
                    <div className="status-icon success">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polyline points="20 6 9 17 4 4"></polyline>
                            <polyline points="20 12 9 17 8 4"></polyline>
                            <polyline points="20 18 9 17 16 4"></polyline>
                        </svg>
                    </div>
                );
            case 'error':
                return (
                    <div className="status-icon error">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="15" y1="9" x2="9" y2="15"></line>
                            <line x1="9" y1="9" x2="15" y2="15"></line>
                        </svg>
                    </div>
                );
            default:
                return (
                    <div className="status-icon idle">
                        <div className="idle-dot"></div>
                    </div>
                );
        }
    };

    return (
        <div className={`data-status-indicator status-${status}`}>
            {getStatusIcon()}
            <div className="status-message">
                {message}
            </div>
        </div>
    );
};

export default DataStatusIndicator;
