import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useConversation } from '../contexts/ConversationContext';
import ChatBox from '../components/ChatBox';
import Sidebar from '../components/Sidebar';
import ResearchPanel from '../components/ResearchPanel';
import './ChatPage.css';

function ChatPage() {
  const { user } = useAuth();
  const { 
    currentConversation, 
    messages, 
    loading, 
    fetchConversations,
    sendMessage,
    createNewConversation 
  } = useConversation();
  
  const [showResearchPanel, setShowResearchPanel] = useState(false);
  const [context, setContext] = useState({});
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (user) {
      fetchConversations(user.id);
    }
  }, [user, fetchConversations]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (message) => {
    if (!user) return;

    const result = await sendMessage(user.id, message, context);
    if (result.success && messages.length === 2) {
      // First successful message, show research panel
      setShowResearchPanel(true);
    }
  };

  const handleNewConversation = () => {
    createNewConversation();
    setShowResearchPanel(false);
    setContext({});
  };

  const handleContextUpdate = (newContext) => {
    setContext(prev => ({ ...prev, ...newContext }));
  };

  const currentResearchData = messages.length > 0 
    ? messages[messages.length - 1]?.content?.research 
    : null;

  return (
    <div className="chat-page">
      <div className="chat-layout">
        {/* Sidebar */}
        <Sidebar 
          user={user}
          onNewConversation={handleNewConversation}
          currentConversationId={currentConversation?.id}
        />

        {/* Main Chat Area */}
        <div className="chat-main">
          <div className="chat-header">
            <div className="header-content">
              <h1 className="header-title">
                AI Medical Research Assistant
              </h1>
              <div className="header-info">
                {currentConversation ? (
                  <span className="conversation-title">
                    {currentConversation.title}
                  </span>
                ) : (
                  <span className="new-conversation-hint">
                    Start a new conversation
                  </span>
                )}
              </div>
            </div>
            
            <div className="header-actions">
              <button
                className={`research-toggle ${showResearchPanel ? 'active' : ''}`}
                onClick={() => setShowResearchPanel(!showResearchPanel)}
                disabled={!currentResearchData}
              >
                <span className="research-icon">Research</span>
                {currentResearchData && (
                  <span className="research-count">
                    {currentResearchData.publications?.length || 0 + 
                     currentResearchData.clinicalTrials?.length || 0} sources
                  </span>
                )}
              </button>
              
              <div className="user-info">
                <span className="user-name">{user?.name}</span>
                <div className="user-avatar">
                  {user?.name?.charAt(0)?.toUpperCase()}
                </div>
              </div>
            </div>
          </div>

          <div className="chat-content">
            <ChatBox
              messages={messages}
              onSendMessage={handleSendMessage}
              loading={loading}
              context={context}
              onContextUpdate={handleContextUpdate}
            />
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Research Panel */}
        {showResearchPanel && currentResearchData && (
          <div className="research-panel-container">
            <ResearchPanel
              researchData={currentResearchData}
              onClose={() => setShowResearchPanel(false)}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatPage;
