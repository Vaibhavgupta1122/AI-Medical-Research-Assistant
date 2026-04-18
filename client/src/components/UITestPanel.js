import React, { useState, useEffect } from 'react';
import './UITestPanel.css';

const UITestPanel = () => {
    const [testResults, setTestResults] = useState({
        scrollButtons: 'unknown',
        dataStatus: 'unknown',
        messageButtons: 'unknown',
        dataFetching: 'unknown',
        responsiveDesign: 'unknown'
    });

    const [isExpanded, setIsExpanded] = useState(false);

    useEffect(() => {
        // Test scroll buttons
        const testScrollButtons = () => {
            const upButton = document.querySelector('.scroll-button-up');
            const downButton = document.querySelector('.scroll-button-down');

            if (upButton && downButton) {
                setTestResults(prev => ({
                    ...prev,
                    scrollButtons: 'working',
                    messageButtons: 'working'
                }));
            } else {
                setTestResults(prev => ({
                    ...prev,
                    scrollButtons: 'missing'
                }));
            }
        };

        // Test data status indicator
        const testDataStatus = () => {
            const statusIndicator = document.querySelector('.data-status-indicator');
            if (statusIndicator) {
                setTestResults(prev => ({
                    ...prev,
                    dataStatus: 'working'
                }));
            } else {
                setTestResults(prev => ({
                    ...prev,
                    dataStatus: 'missing'
                }));
            }
        };

        // Test message buttons
        const testMessageButtons = () => {
            const sendButtons = document.querySelectorAll('.suggestion-btn, .send-button');
            if (sendButtons.length > 0) {
                setTestResults(prev => ({
                    ...prev,
                    messageButtons: 'working'
                }));
            } else {
                setTestResults(prev => ({
                    ...prev,
                    messageButtons: 'missing'
                }));
            }
        };

        // Test data fetching
        const testDataFetching = () => {
            fetch('http://localhost:5000/api/health')
                .then(response => response.json())
                .then(data => {
                    setTestResults(prev => ({
                        ...prev,
                        dataFetching: 'working'
                    }));
                })
                .catch(error => {
                    setTestResults(prev => ({
                        ...prev,
                        dataFetching: 'error'
                    }));
                });
        };

        // Test responsive design
        const testResponsiveDesign = () => {
            const isMobile = window.innerWidth <= 768;
            const hasResponsiveElements = document.querySelectorAll('.chat-layout, .login-container');
            if (hasResponsiveElements.length > 0) {
                setTestResults(prev => ({
                    ...prev,
                    responsiveDesign: isMobile ? 'mobile' : 'desktop'
                }));
            }
        };

        // Run all tests
        setTimeout(() => {
            testScrollButtons();
            testDataStatus();
            testMessageButtons();
            testDataFetching();
            testResponsiveDesign();
        }, 1000);
    }, []);

    const getStatusIcon = (status) => {
        switch (status) {
            case 'working':
                return '✅';
            case 'missing':
                return '❌';
            case 'error':
                return '⚠️';
            case 'mobile':
                return '📱';
            case 'desktop':
                return '🖥️';
            default:
                return '❓';
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'working':
                return '#22c55e';
            case 'missing':
                return '#ef4444';
            case 'error':
                return '#f59e0b';
            default:
                return '#6b7280';
        }
    };

    return (
        <div className={`ui-test-panel ${isExpanded ? 'expanded' : 'collapsed'}`}>
            <button
                className="test-toggle"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <span className="toggle-icon">{isExpanded ? '▼' : '▲'}</span>
                UI Test Panel
            </button>

            {isExpanded && (
                <div className="test-content">
                    <h3>Frontend UI Components Test</h3>

                    <div className="test-grid">
                        <div className="test-item">
                            <span className="test-icon">{getStatusIcon(testResults.scrollButtons)}</span>
                            <span className="test-label">Scroll Buttons</span>
                            <span className="test-status" style={{ color: getStatusColor(testResults.scrollButtons) }}>
                                {testResults.scrollButtons}
                            </span>
                        </div>

                        <div className="test-item">
                            <span className="test-icon">{getStatusIcon(testResults.dataStatus)}</span>
                            <span className="test-label">Data Status Indicator</span>
                            <span className="test-status" style={{ color: getStatusColor(testResults.dataStatus) }}>
                                {testResults.dataStatus}
                            </span>
                        </div>

                        <div className="test-item">
                            <span className="test-icon">{getStatusIcon(testResults.messageButtons)}</span>
                            <span className="test-label">Message Buttons</span>
                            <span className="test-status" style={{ color: getStatusColor(testResults.messageButtons) }}>
                                {testResults.messageButtons}
                            </span>
                        </div>

                        <div className="test-item">
                            <span className="test-icon">{getStatusIcon(testResults.dataFetching)}</span>
                            <span className="test-label">Data Fetching</span>
                            <span className="test-status" style={{ color: getStatusColor(testResults.dataFetching) }}>
                                {testResults.dataFetching}
                            </span>
                        </div>

                        <div className="test-item">
                            <span className="test-icon">{getStatusIcon(testResults.responsiveDesign)}</span>
                            <span className="test-label">Responsive Design</span>
                            <span className="test-status" style={{ color: getStatusColor(testResults.responsiveDesign) }}>
                                {testResults.responsiveDesign}
                            </span>
                        </div>
                    </div>

                    <div className="test-summary">
                        <h4>Summary</h4>
                        <div className="summary-item">
                            <strong>All Components Working:</strong>
                            <span className={Object.values(testResults).every(result => result === 'working') ? 'summary-good' : 'summary-bad'}>
                                {Object.values(testResults).every(result => result === 'working') ? '✅ YES' : '❌ NO'}
                            </span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UITestPanel;
