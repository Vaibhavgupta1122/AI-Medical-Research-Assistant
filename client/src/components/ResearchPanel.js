import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './ResearchPanel.css';

function ResearchPanel({ researchData, onClose }) {
  const [activeTab, setActiveTab] = useState('publications');
  const [expandedItems, setExpandedItems] = useState(new Set());

  const publications = researchData?.publications || [];
  const clinicalTrials = researchData?.clinicalTrials || [];

  const toggleExpand = (id) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedItems(newExpanded);
  };

  const formatAuthors = (authors) => {
    if (!authors || authors.length === 0) return 'Unknown authors';
    if (authors.length <= 2) return authors.join(' & ');
    return `${authors[0]} et al.`;
  };

  const formatYear = (year) => {
    if (!year) return 'Unknown year';
    return year.toString();
  };

  const renderPublication = (pub, index) => {
    const isExpanded = expandedItems.has(pub.id || index);
    
    return (
      <div key={pub.id || index} className="research-item">
        <div className="research-header">
          <div className="research-title">
            <h4>{pub.title}</h4>
            <div className="research-meta">
              <span className="authors">{formatAuthors(pub.authors)}</span>
              <span className="journal">{pub.journal}</span>
              <span className="year">{formatYear(pub.year)}</span>
            </div>
          </div>
          <div className="research-actions">
            <span className="relevance-score">
              {Math.round((pub.relevanceScore || 0) * 100)}% match
            </span>
            <button
              className="expand-btn"
              onClick={() => toggleExpand(pub.id || index)}
            >
              {isExpanded ? 'Collapse' : 'Expand'}
            </button>
          </div>
        </div>
        
        {isExpanded && (
          <div className="research-content">
            {pub.abstract && (
              <div className="research-abstract">
                <h5>Abstract</h5>
                <p>{pub.abstract}</p>
              </div>
            )}
            
            <div className="research-links">
              {pub.doi && (
                <a
                  href={`https://doi.org/${pub.doi}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="research-link"
                >
                  View Article
                </a>
              )}
              {pub.url && (
                <a
                  href={pub.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="research-link"
                >
                  Source
                </a>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderClinicalTrial = (trial, index) => {
    const isExpanded = expandedItems.has(trial.nctId || index);
    
    return (
      <div key={trial.nctId || index} className="research-item clinical-trial">
        <div className="research-header">
          <div className="research-title">
            <h4>{trial.title}</h4>
            <div className="trial-meta">
              <span className="trial-id">NCT {trial.nctId}</span>
              <span className={`status ${trial.status?.toLowerCase().replace(' ', '-')}`}>
                {trial.status}
              </span>
              {trial.phase && (
                <span className="phase">{trial.phase}</span>
              )}
            </div>
          </div>
          <div className="research-actions">
            <span className="relevance-score">
              {Math.round((trial.relevanceScore || 0) * 100)}% match
            </span>
            <button
              className="expand-btn"
              onClick={() => toggleExpand(trial.nctId || index)}
            >
              {isExpanded ? 'Collapse' : 'Expand'}
            </button>
          </div>
        </div>
        
        {isExpanded && (
          <div className="research-content">
            {trial.eligibility && (
              <div className="trial-eligibility">
                <h5>Eligibility Criteria</h5>
                <div className="markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {trial.eligibility}
                  </ReactMarkdown>
                </div>
              </div>
            )}
            
            {trial.conditions && trial.conditions.length > 0 && (
              <div className="trial-conditions">
                <h5>Conditions</h5>
                <div className="condition-tags">
                  {trial.conditions.map((condition, idx) => (
                    <span key={idx} className="condition-tag">
                      {condition}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            {trial.contacts && trial.contacts.length > 0 && (
              <div className="trial-contacts">
                <h5>Contact Information</h5>
                {trial.contacts.map((contact, idx) => (
                  <div key={idx} className="contact-item">
                    {contact.name && <span className="contact-name">{contact.name}</span>}
                    {contact.email && <span className="contact-email">{contact.email}</span>}
                    {contact.phone && <span className="contact-phone">{contact.phone}</span>}
                  </div>
                ))}
              </div>
            )}
            
            <div className="research-links">
              <a
                href={`https://clinicaltrials.gov/study/${trial.nctId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="research-link"
              >
                View Trial Details
              </a>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="research-panel">
      <div className="research-header">
        <h3>Research Sources</h3>
        <button className="close-btn" onClick={onClose}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div className="research-tabs">
        <button
          className={`tab ${activeTab === 'publications' ? 'active' : ''}`}
          onClick={() => setActiveTab('publications')}
        >
          Publications ({publications.length})
        </button>
        <button
          className={`tab ${activeTab === 'trials' ? 'active' : ''}`}
          onClick={() => setActiveTab('trials')}
        >
          Clinical Trials ({clinicalTrials.length})
        </button>
      </div>

      <div className="research-content">
        {activeTab === 'publications' && (
          <div className="research-list">
            {publications.length === 0 ? (
              <div className="empty-state">
                <p>No publications found for this query.</p>
              </div>
            ) : (
              publications.map(renderPublication)
            )}
          </div>
        )}

        {activeTab === 'trials' && (
          <div className="research-list">
            {clinicalTrials.length === 0 ? (
              <div className="empty-state">
                <p>No clinical trials found for this query.</p>
              </div>
            ) : (
              clinicalTrials.map(renderClinicalTrial)
            )}
          </div>
        )}
      </div>

      <div className="research-footer">
        <div className="research-summary">
          <p>
            Found {publications.length} publications and {clinicalTrials.length} clinical trials.
            Sources are ranked by relevance to your query.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ResearchPanel;
