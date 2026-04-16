const express = require('express');
const Conversation = require('../models/Conversation');
const Message = require('../models/Message');
const User = require('../models/User');

const router = express.Router();

// GET /api/conversations/:id - Get specific conversation with messages
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { userId } = req.query;

    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }

    const conversation = await Conversation.findOne({ 
      _id: id, 
      userId,
      status: { $ne: 'deleted' }
    }).lean();

    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    // Get messages for this conversation
    const messages = await Message.find({ conversationId: id })
      .sort({ createdAt: 1 })
      .select('type content metadata createdAt')
      .lean();

    res.json({
      success: true,
      conversation,
      messages
    });

  } catch (error) {
    console.error('Get Conversation Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /api/conversations/:id - Update conversation
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { userId, title, context, tags, isBookmarked } = req.body;

    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }

    const conversation = await Conversation.findOne({ 
      _id: id, 
      userId 
    });

    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    // Update allowed fields
    if (title) conversation.title = title;
    if (context) conversation.context = { ...conversation.context, ...context };
    if (tags) conversation.tags = tags;
    if (typeof isBookmarked === 'boolean') conversation.isBookmarked = isBookmarked;

    await conversation.save();

    res.json({
      success: true,
      conversation
    });

  } catch (error) {
    console.error('Update Conversation Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /api/conversations/:id - Soft delete conversation
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { userId } = req.body;

    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }

    const conversation = await Conversation.findOne({ 
      _id: id, 
      userId 
    });

    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    conversation.status = 'deleted';
    await conversation.save();

    res.json({
      success: true,
      message: 'Conversation deleted successfully'
    });

  } catch (error) {
    console.error('Delete Conversation Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /api/conversations/:id/feedback - Add feedback to conversation
router.post('/:id/feedback', async (req, res) => {
  try {
    const { id } = req.params;
    const { userId, rating, comments } = req.body;

    if (!userId || !rating) {
      return res.status(400).json({ error: 'userId and rating are required' });
    }

    const conversation = await Conversation.findOne({ 
      _id: id, 
      userId 
    });

    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    conversation.metadata.satisfactionRating = rating;
    await conversation.save();

    res.json({
      success: true,
      message: 'Feedback recorded successfully'
    });

  } catch (error) {
    console.error('Feedback Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
