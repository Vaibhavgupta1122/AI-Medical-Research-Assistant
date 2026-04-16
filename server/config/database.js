const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log(`MongoDB Connected: ${conn.connection.host}`);
    
    // Create indexes for better performance
    await createIndexes();
    
  } catch (error) {
    console.error('Database connection error:', error);
    process.exit(1);
  }
};

const createIndexes = async () => {
  try {
    // User indexes
    await mongoose.connection.db.collection('users').createIndex({ email: 1 }, { unique: true });
    await mongoose.connection.db.collection('users').createIndex({ 'profile.location.country': 1 });
    
    // Conversation indexes
    await mongoose.connection.db.collection('conversations').createIndex({ userId: 1, createdAt: -1 });
    await mongoose.connection.db.collection('conversations').createIndex({ 'context.primaryCondition': 1 });
    
    // Message indexes
    await mongoose.connection.db.collection('messages').createIndex({ conversationId: 1, createdAt: 1 });
    
    console.log('Database indexes created successfully');
  } catch (error) {
    console.error('Error creating indexes:', error);
  }
};

module.exports = connectDB;
