const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Mock data for testing
const mockUsers = [
  { id: '1', name: 'Test User', email: 'test@example.com' }
];

const mockConversations = [
  {
    id: '1',
    userId: '1',
    title: 'Test Conversation',
    createdAt: new Date().toISOString(),
    messages: [
      { id: '1', type: 'user', content: { text: 'Hello' }, timestamp: new Date().toISOString() },
      { id: '2', type: 'assistant', content: { text: 'Hi! How can I help you today?' }, timestamp: new Date().toISOString() }
    ]
  }
];

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', message: 'Backend running without MongoDB' });
});

// Auth routes (mock)
app.post('/api/auth/register', (req, res) => {
  const { name, email, password } = req.body;
  const user = { id: Date.now().toString(), name, email };
  res.json({ success: true, user, token: 'mock-token' });
});

app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  const user = mockUsers.find(u => u.email === email);
  if (user) {
    res.json({ success: true, user, token: 'mock-token' });
  } else {
    res.status(401).json({ success: false, message: 'Invalid credentials' });
  }
});

// Chat routes (mock)
app.post('/api/chat', async (req, res) => {
  const { userId, message, context } = req.body;
  
  // Call AI service
  try {
    const response = await fetch('http://localhost:8000/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: message, context })
    });
    
    const aiResponse = await response.json();
    
    res.json({
      success: true,
      conversationId: '1',
      message: {
        id: Date.now().toString(),
        type: 'assistant',
        content: { text: aiResponse.answer, research: aiResponse.sources },
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    res.json({
      success: true,
      conversationId: '1',
      message: {
        id: Date.now().toString(),
        type: 'assistant',
        content: { text: 'AI service unavailable. Please check if the AI service is running on port 8000.' },
        timestamp: new Date().toISOString()
      }
    });
  }
});

app.get('/api/history/:userId', (req, res) => {
  res.json({ success: true, conversations: mockConversations });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('Mock mode - No MongoDB required');
});
