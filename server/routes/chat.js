const express = require('express');
const axios = require('axios');
const Message = require('../models/Message');
const Conversation = require('../models/Conversation');
const User = require('../models/User');

const router = express.Router();

// POST /api/chat - Send a message and get AI response
router.post('/', async (req, res) => {
  try {
    const { userId, conversationId, message, context } = req.body;

    if (!userId || !message) {
      return res.status(400).json({ error: 'userId and message are required' });
    }

    // Verify user exists
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Get or create conversation
    let conversation;
    if (conversationId) {
      conversation = await Conversation.findById(conversationId);
      if (!conversation || conversation.userId.toString() !== userId) {
        return res.status(404).json({ error: 'Conversation not found' });
      }
    } else {
      // Create new conversation
      conversation = new Conversation({
        userId,
        title: message.substring(0, 100) + (message.length > 100 ? '...' : ''),
        context: {
          primaryCondition: context?.primaryCondition || 'General medical inquiry',
          secondaryConditions: context?.secondaryConditions || [],
          symptoms: context?.symptoms || [],
          medications: context?.medications || [],
          location: context?.location || user.profile.location || {},
          demographicInfo: context?.demographicInfo || {
            age: user.profile.age,
            gender: user.profile.gender
          }
        }
      });
      await conversation.save();
    }

    // Save user message
    const userMessage = new Message({
      conversationId: conversation._id,
      type: 'user',
      content: {
        text: message,
        structuredData: {
          query: {
            original: message,
            expanded: message, // Will be enhanced by AI service
            intent: 'general_inquiry'
          }
        }
      }
    });
    await userMessage.save();

    // Get conversation history for context
    const recentMessages = await Message.find({ conversationId: conversation._id })
      .sort({ createdAt: -1 })
      .limit(10)
      .lean();

    // Call AI service
    try {
      const aiResponse = await axios.post(`${process.env.AI_SERVICE_URL}/research`, {
        message,
        conversationHistory: recentMessages.reverse(),
        context: conversation.context,
        userId
      }, {
        timeout: 60000, // 60 second timeout
        headers: {
          'Content-Type': 'application/json'
        }
      });

      // Save AI response
      const assistantMessage = new Message({
        conversationId: conversation._id,
        type: 'assistant',
        content: {
          text: aiResponse.data.answer,
          structuredData: {
            research: aiResponse.data.research
          }
        },
        metadata: {
          processingTime: aiResponse.data.processingTime,
          tokensUsed: aiResponse.data.tokensUsed,
          modelUsed: aiResponse.data.modelUsed,
          sources: aiResponse.data.sources,
          confidence: aiResponse.data.confidence
        }
      });
      await assistantMessage.save();

      // Update conversation metadata
      conversation.metadata.totalMessages += 2;
      conversation.metadata.lastActivity = new Date();
      conversation.researchData.totalPapersRetrieved += aiResponse.data.research?.publications?.length || 0;
      conversation.researchData.totalClinicalTrialsFound += aiResponse.data.research?.clinicalTrials?.length || 0;
      conversation.researchData.lastResearchDate = new Date();
      await conversation.save();

      // Update user usage stats
      user.usage.totalQueries += 1;
      user.usage.queriesThisMonth += 1;
      user.usage.lastQueryDate = new Date();
      await user.save();

      res.json({
        success: true,
        conversationId: conversation._id,
        response: {
          id: assistantMessage._id,
          message: aiResponse.data.answer,
          research: aiResponse.data.research,
          metadata: assistantMessage.metadata,
          timestamp: assistantMessage.createdAt
        }
      });

    } catch (aiError) {
      console.error('AI Service Error:', aiError.message);
      
      // Save error message
      const errorMessage = new Message({
        conversationId: conversation._id,
        type: 'assistant',
        content: {
          text: 'I apologize, but I\'m currently unable to process your research request. Please try again in a few moments.',
          structuredData: {}
        },
        metadata: {
          error: true,
          errorMessage: aiError.message
        }
      });
      await errorMessage.save();

      res.status(503).json({
        error: 'AI service temporarily unavailable',
        conversationId: conversation._id
      });
    }

  } catch (error) {
    console.error('Chat Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/chat/history/:userId - Get user's conversation history
router.get('/history/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const { limit = 20, offset = 0 } = req.query;

    const conversations = await Conversation.find({ 
      userId, 
      status: { $ne: 'deleted' } 
    })
    .sort({ 'metadata.lastActivity': -1 })
    .limit(parseInt(limit))
    .skip(parseInt(offset))
    .select('title context metadata createdAt')
    .lean();

    res.json({
      success: true,
      conversations,
      total: await Conversation.countDocuments({ 
        userId, 
        status: { $ne: 'deleted' } 
      })
    });

  } catch (error) {
    console.error('History Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
