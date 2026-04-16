const express = require('express');
const User = require('../models/User');
const jwt = require('jsonwebtoken');

const router = express.Router();

// Simple JWT secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// POST /api/auth/register - Register new user
router.post('/register', async (req, res) => {
  try {
    const { email, name, profile } = req.body;

    if (!email || !name) {
      return res.status(400).json({ error: 'Email and name are required' });
    }

    // Check if user already exists
    const existingUser = await User.findOne({ email: email.toLowerCase() });
    if (existingUser) {
      return res.status(409).json({ error: 'User already exists' });
    }

    // Create new user
    const user = new User({
      email: email.toLowerCase(),
      name: name.trim(),
      profile: profile || {},
      usage: {
        totalQueries: 0,
        queriesThisMonth: 0
      }
    });

    await user.save();

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, email: user.email },
      JWT_SECRET,
      { expiresIn: '30d' }
    );

    res.status(201).json({
      success: true,
      token,
      user: {
        id: user._id,
        email: user.email,
        name: user.name,
        profile: user.profile,
        subscription: user.subscription,
        usage: user.usage
      }
    });

  } catch (error) {
    console.error('Registration Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /api/auth/login - Login user
router.post('/login', async (req, res) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ error: 'Email is required' });
    }

    // Find user
    const user = await User.findOne({ email: email.toLowerCase() });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, email: user.email },
      JWT_SECRET,
      { expiresIn: '30d' }
    );

    res.json({
      success: true,
      token,
      user: {
        id: user._id,
        email: user.email,
        name: user.name,
        profile: user.profile,
        subscription: user.subscription,
        usage: user.usage
      }
    });

  } catch (error) {
    console.error('Login Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Middleware to verify JWT token
const verifyToken = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'Access denied. No token provided.' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// GET /api/auth/verify - Verify token and get user info
router.get('/verify', verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId).select('-__v');
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      success: true,
      user: {
        id: user._id,
        email: user.email,
        name: user.name,
        profile: user.profile,
        subscription: user.subscription,
        usage: user.usage
      }
    });

  } catch (error) {
    console.error('Token Verification Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
module.exports.verifyToken = verifyToken;
