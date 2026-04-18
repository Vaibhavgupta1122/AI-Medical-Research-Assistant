const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI, {
      serverSelectionTimeoutMS: 5000, // Keep trying to send operations for 5 seconds
      maxPoolSize: 10, // Maintain up to 10 socket connections
    });

    console.log(`MongoDB Connected: ${conn.connection.host}`);

    // Create indexes for better performance
    await createIndexes();

  } catch (error) {
    console.error('Database connection error:', error.message);
    // Don't exit the process, let the server continue without DB initially
    console.log('Server will continue running without database connection...');
  }
};

const createIndexes = async () => {
  try {
    // Only create indexes if connected to database
    if (mongoose.connection.readyState !== 1) {
      console.log('Skipping index creation - database not connected');
      return;
    }

    // User indexes
    await mongoose.connection.db.collection('users').createIndex({ 'profile.location.country': 1 });

    // Conversation indexes
    await mongoose.connection.db.collection('conversations').createIndex({ userId: 1, createdAt: -1 });
    await mongoose.connection.db.collection('conversations').createIndex({ 'context.primaryCondition': 1 });

    // Message indexes
    await mongoose.connection.db.collection('messages').createIndex({ conversationId: 1, createdAt: 1 });

    console.log('Database indexes created successfully');
  } catch (error) {
    console.error('Error creating indexes:', error.message);
  }
};

// Retry connection function
const retryConnection = async () => {
  if (mongoose.connection.readyState === 0) { // Disconnected
    console.log('Attempting to reconnect to database...');
    await connectDB();
  }
};

// Set up periodic reconnection attempts
setInterval(retryConnection, 30000); // Try to reconnect every 30 seconds

module.exports = connectDB;
