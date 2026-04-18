import React from 'react';
import './ScrollButton.css';

const ScrollButton = ({ onClick, direction, disabled = false }) => {
    return (
        <button
            className={`scroll-button scroll-button-${direction} ${disabled ? 'disabled' : ''}`}
            onClick={onClick}
            disabled={disabled}
            title={`Scroll ${direction}`}
        >
            <svg
                className="scroll-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            >
                {direction === 'up' ? (
                    <polyline points="18 15 12 9 6 6"></polyline>
                ) : (
                    <polyline points="6 9 12 15 18"></polyline>
                )}
            </svg>
        </button>
    );
};

export default ScrollButton;
