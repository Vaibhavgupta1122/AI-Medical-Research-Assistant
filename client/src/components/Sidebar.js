import React, { useState } from 'react';
import { useConversation } from '../contexts/ConversationContext';
import { useAuth } from '../contexts/AuthContext';
import './Sidebar.css';

function Sidebar({ user, onNewConversation, currentConversationId }) {
  const { conversations, loading, fetchConversation, deleteConversation } = useConversation();
  const { logout } = useAuth();
  const [showConfirmDelete, setShowConfirmDelete] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredConversations = conversations.filter(conv =>
    conv.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleConversationClick = (conversationId) => {
    if (conversationId !== currentConversationId) {
      fetchConversation(conversationId, user.id);
    }
  };

  const handleDeleteConversation = async (conversationId, e) => {
    e.stopPropagation();
    
    if (showConfirmDelete === conversationId) {
      const result = await deleteConversation(conversationId, user.id);
      if (result.success) {
        setShowConfirmDelete(null);
      }
    } else {
      setShowConfirmDelete(conversationId);
    }
  };

  const handleLogout = () => {
    logout();
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays <= 7) return `${diffDays - 1} days ago`;
    if (diffDays <= 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="user-section">
          <div className="user-avatar">
            {user?.name?.charAt(0)?.toUpperCase()}
          </div>
          <div className="user-info">
            <div className="user-name">{user?.name}</div>
            <div className="user-email">{user?.email}</div>
          </div>
        </div>
        
        <button className="logout-btn" onClick={handleLogout} title="Logout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>

      <div className="sidebar-content">
        <div className="new-conversation-section">
          <button className="new-conversation-btn" onClick={onNewConversation}>
            <svg className="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            New Conversation
          </button>
        </div>

        <div className="conversations-section">
          <div className="section-header">
            <h3>Recent Conversations</h3>
            <div className="conversation-count">
              {filteredConversations.length}
            </div>
          </div>

          <div className="search-container">
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>

          <div className="conversations-list">
            {loading ? (
              <div className="loading-state">
                <div className="loading-spinner"></div>
                <span>Loading conversations...</span>
              </div>
            ) : filteredConversations.length === 0 ? (
              <div className="empty-state">
                {searchTerm ? 'No conversations found' : 'No conversations yet'}
              </div>
            ) : (
              filteredConversations.map((conversation) => (
                <div
                  key={conversation.id}
                  className={`conversation-item ${conversation.id === currentConversationId ? 'active' : ''}`}
                  onClick={() => handleConversationClick(conversation.id)}
                >
                  <div className="conversation-content">
                    <div className="conversation-title">
                      {conversation.title}
                    </div>
                    <div className="conversation-meta">
                      <span className="conversation-date">
                        {formatDate(conversation.metadata?.lastActivity || conversation.createdAt)}
                      </span>
                      <span className="message-count">
                        {conversation.metadata?.totalMessages || 0} messages
                      </span>
                    </div>
                    {conversation.context?.primaryCondition && (
                      <div className="conversation-condition">
                        {conversation.context.primaryCondition}
                      </div>
                    )}
                  </div>
                  
                  <div className="conversation-actions">
                    {showConfirmDelete === conversation.id ? (
                      <div className="confirm-delete">
                        <span>Delete?</span>
                        <button
                          className="confirm-yes"
                          onClick={(e) => handleDeleteConversation(conversation.id, e)}
                        >
                          Yes
                        </button>
                        <button
                          className="confirm-no"
                          onClick={(e) => {
                            e.stopPropagation();
                            setShowConfirmDelete(null);
                          }}
                        >
                          No
                        </button>
                      </div>
                    ) : (
                      <button
                        className="delete-btn"
                        onClick={(e) => handleDeleteConversation(conversation.id, e)}
                        title="Delete conversation"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
