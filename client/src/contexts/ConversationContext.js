import React, { createContext, useContext, useState, useCallback } from 'react';
import { chatAPI } from '../services/api';

const ConversationContext = createContext();

export function useConversation() {
  return useContext(ConversationContext);
}

export function ConversationProvider({ children }) {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchConversations = useCallback(async (userId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await chatAPI.getHistory(userId);
      if (response.data.success) {
        setConversations(response.data.conversations);
      }
    } catch (error) {
      console.error('Error fetching conversations:', error);
      setError('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchConversation = useCallback(async (conversationId, userId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await chatAPI.getConversation(conversationId, userId);
      if (response.data.success) {
        setCurrentConversation(response.data.conversation);
        setMessages(response.data.messages);
      }
    } catch (error) {
      console.error('Error fetching conversation:', error);
      setError('Failed to load conversation');
    } finally {
      setLoading(false);
    }
  }, []);

  const sendMessage = useCallback(async (userId, message, context = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      // Add user message optimistically
      const userMessage = {
        id: Date.now(),
        type: 'user',
        content: { text: message },
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, userMessage]);

      // Add typing indicator
      const typingMessage = {
        id: 'typing',
        type: 'assistant',
        content: { text: '' },
        timestamp: new Date().toISOString(),
        isTyping: true
      };
      setMessages(prev => [...prev, typingMessage]);

      const response = await chatAPI.sendMessage(userId, currentConversation?.id, message, context);
      
      // Remove typing indicator
      setMessages(prev => prev.filter(msg => msg.id !== 'typing'));

      if (response.data.success) {
        const assistantMessage = {
          id: response.data.response.id,
          type: 'assistant',
          content: {
            text: response.data.response.message,
            research: response.data.response.research
          },
          metadata: response.data.response.metadata,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, assistantMessage]);

        // Update current conversation if new
        if (!currentConversation) {
          setCurrentConversation({
            id: response.data.conversationId,
            title: message.substring(0, 100) + (message.length > 100 ? '...' : ''),
            context
          });
        }

        return { success: true };
      } else {
        throw new Error(response.data.error || 'Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Remove typing indicator
      setMessages(prev => prev.filter(msg => msg.id !== 'typing'));
      
      // Add error message
      const errorMessage = {
        id: Date.now(),
        type: 'assistant',
        content: { text: 'Sorry, I encountered an error. Please try again.' },
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
      
      setError('Failed to send message');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, [currentConversation]);

  const createNewConversation = useCallback(() => {
    setCurrentConversation(null);
    setMessages([]);
    setError(null);
  }, []);

  const updateConversation = useCallback(async (conversationId, updates) => {
    try {
      const response = await chatAPI.updateConversation(conversationId, updates);
      if (response.data.success) {
        if (currentConversation && currentConversation.id === conversationId) {
          setCurrentConversation(prev => ({ ...prev, ...updates }));
        }
        return { success: true };
      }
      return { success: false, error: 'Failed to update conversation' };
    } catch (error) {
      console.error('Error updating conversation:', error);
      return { success: false, error: error.message };
    }
  }, [currentConversation]);

  const deleteConversation = useCallback(async (conversationId, userId) => {
    try {
      const response = await chatAPI.deleteConversation(conversationId, userId);
      if (response.data.success) {
        setConversations(prev => prev.filter(conv => conv.id !== conversationId));
        if (currentConversation && currentConversation.id === conversationId) {
          createNewConversation();
        }
        return { success: true };
      }
      return { success: false, error: 'Failed to delete conversation' };
    } catch (error) {
      console.error('Error deleting conversation:', error);
      return { success: false, error: error.message };
    }
  }, [currentConversation, createNewConversation]);

  const value = {
    conversations,
    currentConversation,
    messages,
    loading,
    error,
    fetchConversations,
    fetchConversation,
    sendMessage,
    createNewConversation,
    updateConversation,
    deleteConversation,
    setError
  };

  return (
    <ConversationContext.Provider value={value}>
      {children}
    </ConversationContext.Provider>
  );
}
