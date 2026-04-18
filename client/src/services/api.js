import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 60000, // 60 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email) => api.post('/auth/login', { email }),
  register: (email, name, profile) => api.post('/auth/register', { email, name, profile }),
  verifyToken: (token) => api.get('/auth/verify'),
};

// Chat API
export const chatAPI = {
  sendMessage: (userId, conversationId, message, context) =>
    api.post('/chat', { userId, conversationId, message, context }),

  getHistory: (userId, limit = 20, offset = 0) =>
    api.get(`/chat/history/${userId}?limit=${limit}&offset=${offset}`),

  getConversation: (conversationId, userId) =>
    api.get(`/conversations/${conversationId}?userId=${userId}`),

  updateConversation: (conversationId, updates) =>
    api.put(`/conversations/${conversationId}`, updates),

  deleteConversation: (conversationId, userId) =>
    api.delete(`/conversations/${conversationId}`, { data: { userId } }),

  addFeedback: (conversationId, userId, rating, comments) =>
    api.post(`/conversations/${conversationId}/feedback`, { userId, rating, comments }),
};

// User API
export const userAPI = {
  getProfile: (userId) => api.get(`/users/${userId}`),
  updateProfile: (userId, profile, preferences) =>
    api.put(`/users/${userId}`, { profile, preferences }),
  getStats: (userId) => api.get(`/users/${userId}/stats`),
};

export default api;
