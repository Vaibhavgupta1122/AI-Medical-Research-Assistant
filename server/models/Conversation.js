const mongoose = require('mongoose');

const conversationSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  title: {
    type: String,
    required: true,
    trim: true,
    maxlength: 200
  },
  context: {
    primaryCondition: {
      type: String,
      required: true
    },
    secondaryConditions: [String],
    symptoms: [String],
    medications: [String],
    location: {
      country: String,
      state: String,
      city: String
    },
    demographicInfo: {
      age: Number,
      gender: String
    }
  },
  metadata: {
    totalMessages: { type: Number, default: 0 },
    lastActivity: { type: Date, default: Date.now },
    sessionDuration: Number, // in minutes
    satisfactionRating: {
      type: Number,
      min: 1,
      max: 5
    }
  },
  researchData: {
    totalPapersRetrieved: { type: Number, default: 0 },
    totalClinicalTrialsFound: { type: Number, default: 0 },
    lastResearchDate: Date,
    researchTopics: [String]
  },
  status: {
    type: String,
    enum: ['active', 'archived', 'deleted'],
    default: 'active'
  },
  tags: [String],
  isBookmarked: { type: Boolean, default: false }
}, {
  timestamps: true
});

// Indexes for efficient queries
conversationSchema.index({ userId: 1, createdAt: -1 });
conversationSchema.index({ 'context.primaryCondition': 1 });
conversationSchema.index({ 'context.location.country': 1 });
conversationSchema.index({ tags: 1 });
conversationSchema.index({ status: 1 });

module.exports = mongoose.model('Conversation', conversationSchema);
