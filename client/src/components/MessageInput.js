import React, { useState, useRef, useEffect } from 'react';
import './MessageInput.css';

function MessageInput({ onSendMessage, disabled, placeholder }) {
  const [message, setMessage] = useState('');
  const [isComposing, setIsComposing] = useState(false);
  const textareaRef = useRef(null);

  useEffect(() => {
    // Auto-resize textarea
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, [message]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim() || disabled || isComposing) {
      return;
    }

    const messageToSend = message.trim();
    setMessage('');
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    await onSendMessage(messageToSend);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !isComposing) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleCompositionStart = () => {
    setIsComposing(true);
  };

  const handleCompositionEnd = () => {
    setIsComposing(false);
  };

  return (
    <form onSubmit={handleSubmit} className="message-input-form">
      <div className="message-input-container">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onCompositionStart={handleCompositionStart}
            onCompositionEnd={handleCompositionEnd}
            placeholder={placeholder}
            className="message-textarea"
            disabled={disabled}
            rows={1}
            maxLength={2000}
          />
          
          <div className="input-actions">
            <button
              type="submit"
              className="send-button"
              disabled={!message.trim() || disabled}
              title="Send message (Enter)"
            >
              <svg
                className="send-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
        
        <div className="input-footer">
          <div className="input-hints">
            <span className="hint-text">
              Press Enter to send, Shift+Enter for new line
            </span>
            <span className="character-count">
              {message.length}/2000
            </span>
          </div>
        </div>
      </div>
    </form>
  );
}

export default MessageInput;
