const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  name: {
    type: String,
    required: true,
    trim: true
  },
  profile: {
    age: Number,
    gender: {
      type: String,
      enum: ['male', 'female', 'other', 'prefer_not_to_say']
    },
    location: {
      country: String,
      state: String,
      city: String
    },
    medicalBackground: {
      conditions: [String],
      medications: [String],
      allergies: [String]
    }
  },
  preferences: {
    language: {
      type: String,
      default: 'english'
    },
    complexity: {
      type: String,
      enum: ['basic', 'intermediate', 'advanced'],
      default: 'intermediate'
    },
    notificationSettings: {
      email: { type: Boolean, default: true },
      researchUpdates: { type: Boolean, default: true }
    }
  },
  subscription: {
    plan: {
      type: String,
      enum: ['free', 'premium'],
      default: 'free'
    },
    startDate: Date,
    endDate: Date
  },
  usage: {
    totalQueries: { type: Number, default: 0 },
    queriesThisMonth: { type: Number, default: 0 },
    lastQueryDate: Date
  }
}, {
  timestamps: true
});

// Index for efficient queries
userSchema.index({ 'profile.location.country': 1 });
userSchema.index({ 'profile.medicalBackground.conditions': 1 });

module.exports = mongoose.model('User', userSchema);
