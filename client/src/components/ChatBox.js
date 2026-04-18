import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import MessageInput from './MessageInput';
import ContextPanel from './ContextPanel';
import './ChatBox.css';

function ChatBox({ messages, onSendMessage, loading, context, onContextUpdate }) {
  const [showContextPanel, setShowContextPanel] = useState(false);
  const messagesContainerRef = useRef(null);

  const handleSendMessage = async (message) => {
    await onSendMessage(message);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };


  const renderMessage = (message, index) => {
    const isUser = message.type === 'user';
    const isTyping = message.isTyping;
    const isError = message.isError;

    return (
      <div
        key={message.id || index}
        className={`message ${isUser ? 'user-message' : 'assistant-message'} ${isError ? 'error-message' : ''}`}
      >
        <div className="message-content">
          {!isUser && (
            <div className="message-avatar">
              {isTyping ? (
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              ) : (
                <div className="ai-avatar">
                  <span className="ai-icon">AI</span>
                </div>
              )}
            </div>
          )}

          <div className="message-body">
            {isTyping ? (
              <div className="typing-message">
                <span>Researching medical literature...</span>
              </div>
            ) : (
              <div className="message-text">
                {isUser ? (
                  <p>{message.content.text}</p>
                ) : (
                  <div className="markdown-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.content.text}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            )}

            <div className="message-meta">
              <span className="message-time">
                {formatTimestamp(message.timestamp)}
              </span>
              {message.metadata && (
                <div className="message-metadata">
                  {message.metadata.sources && (
                    <span className="sources-info">
                      {message.metadata.sources.length} sources
                    </span>
                  )}
                  {message.metadata.confidence && (
                    <span className="confidence-info">
                      {Math.round(message.metadata.confidence * 100)}% confidence
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="chat-box">
      <div className="chat-messages" ref={messagesContainerRef}>
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-content">
              <div className="empty-icon">
                <span className="medical-cross">+</span>
              </div>
              <h2>Welcome to AI Medical Research Assistant</h2>
              <p>
                Ask me about medical conditions, treatments, clinical trials, or latest research findings.
                I'll provide evidence-based information from peer-reviewed sources.
              </p>

              <div className="suggested-queries">
                <h3>Try asking:</h3>
                <div className="query-suggestions">
                  <button
                    className="suggestion-btn"
                    onClick={() => handleSendMessage("What are the latest treatments for Parkinson disease?")}
                  >
                    What are the latest treatments for Parkinson disease?
                  </button>
                  <button
                    className="suggestion-btn"
                    onClick={() => handleSendMessage("Are there any clinical trials for Alzheimer's near me?")}
                  >
                    Are there any clinical trials for Alzheimer's near me?
                  </button>
                  <button
                    className="suggestion-btn"
                    onClick={() => handleSendMessage("What does the research say about diabetes management?")}
                  >
                    What does the research say about diabetes management?
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message, index) => renderMessage(message, index))}
            {loading && (
              <div className="message assistant-message">
                <div className="message-content">
                  <div className="message-avatar">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                  <div className="message-body">
                    <div className="typing-message">
                      <span>Analyzing medical literature...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="chat-input-area">
        <div className="input-container">
          <div className="context-toggle">
            <button
              className={`context-btn ${showContextPanel ? 'active' : ''}`}
              onClick={() => setShowContextPanel(!showContextPanel)}
            >
              <span className="context-icon">Context</span>
            </button>
          </div>

          <MessageInput
            onSendMessage={handleSendMessage}
            disabled={loading}
            placeholder="Ask about medical research, treatments, or clinical trials..."
          />
        </div>

        {showContextPanel && (
          <ContextPanel
            context={context}
            onUpdate={onContextUpdate}
            onClose={() => setShowContextPanel(false)}
          />
        )}
      </div>
    </div>
  );
}

export default ChatBox;
