const express = require('express');
const User = require('../models/User');
const { verifyToken } = require('./auth');

const router = express.Router();

// GET /api/users/:id - Get user profile
router.get('/:id', verifyToken, async (req, res) => {
  try {
    const { id } = req.params;

    if (req.user.userId !== id) {
      return res.status(403).json({ error: 'Access denied' });
    }

    const user = await User.findById(id).select('-__v');
    
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
        preferences: user.preferences,
        subscription: user.subscription,
        usage: user.usage,
        createdAt: user.createdAt
      }
    });

  } catch (error) {
    console.error('Get User Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /api/users/:id - Update user profile
router.put('/:id', verifyToken, async (req, res) => {
  try {
    const { id } = req.params;
    const { profile, preferences } = req.body;

    if (req.user.userId !== id) {
      return res.status(403).json({ error: 'Access denied' });
    }

    const user = await User.findById(id);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Update allowed fields
    if (profile) {
      user.profile = { ...user.profile, ...profile };
    }
    
    if (preferences) {
      user.preferences = { ...user.preferences, ...preferences };
    }

    await user.save();

    res.json({
      success: true,
      user: {
        id: user._id,
        email: user.email,
        name: user.name,
        profile: user.profile,
        preferences: user.preferences,
        subscription: user.subscription,
        usage: user.usage
      }
    });

  } catch (error) {
    console.error('Update User Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/users/:id/stats - Get user statistics
router.get('/:id/stats', verifyToken, async (req, res) => {
  try {
    const { id } = req.params;

    if (req.user.userId !== id) {
      return res.status(403).json({ error: 'Access denied' });
    }

    const user = await User.findById(id).select('usage subscription');
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Get conversation stats
    const Conversation = require('../models/Conversation');
    const conversationStats = await Conversation.aggregate([
      { $match: { userId: user._id, status: { $ne: 'deleted' } } },
      {
        $group: {
          _id: null,
          totalConversations: { $sum: 1 },
          avgMessagesPerConversation: { $avg: '$metadata.totalMessages' },
          bookmarkedConversations: { $sum: { $cond: ['$isBookmarked', 1, 0] } }
        }
      }
    ]);

    const stats = conversationStats[0] || {
      totalConversations: 0,
      avgMessagesPerConversation: 0,
      bookmarkedConversations: 0
    };

    res.json({
      success: true,
      stats: {
        ...stats,
        usage: user.usage,
        subscription: user.subscription
      }
    });

  } catch (error) {
    console.error('Get User Stats Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
