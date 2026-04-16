const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema({
  conversationId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Conversation',
    required: true,
    index: true
  },
  type: {
    type: String,
    enum: ['user', 'assistant', 'system'],
    required: true
  },
  content: {
    text: {
      type: String,
      required: function() {
        return this.type !== 'system';
      }
    },
    structuredData: {
      query: {
        original: String,
        expanded: String,
        intent: String,
        entities: [{
          type: String, // disease, symptom, medication, etc.
          value: String,
          confidence: Number
        }]
      },
      research: {
        publications: [{
          id: String,
          title: String,
          authors: [String],
          journal: String,
          year: Number,
          abstract: String,
          doi: String,
          relevanceScore: Number,
          source: String // pubmed, openalex
        }],
        clinicalTrials: [{
          nctId: String,
          title: String,
          status: String,
          phase: String,
          conditions: [String],
          location: String,
          eligibility: String,
          contacts: [{
            name: String,
            email: String,
            phone: String
          }],
          relevanceScore: Number
        }]
      }
    }
  },
  metadata: {
    processingTime: Number, // in milliseconds
    tokensUsed: Number,
    modelUsed: String,
    confidence: Number,
    sources: [String],
    disclaimer: String
  },
  feedback: {
    helpful: {
      type: Number,
      min: 1,
      max: 5
    },
    comments: String,
    reported: { type: Boolean, default: false },
    reportReason: String
  },
  isEdited: { type: Boolean, default: false },
  editHistory: [{
    content: String,
    timestamp: Date,
    reason: String
  }]
}, {
  timestamps: true
});

// Indexes for efficient queries
messageSchema.index({ conversationId: 1, createdAt: 1 });
messageSchema.index({ type: 1 });
messageSchema.index({ 'content.research.publications.id': 1 });
messageSchema.index({ 'content.research.clinicalTrials.nctId': 1 });

module.exports = mongoose.model('Message', messageSchema);
