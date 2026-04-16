#!/bin/bash

echo "Setting up AI Medical Research Assistant..."

# Install MongoDB if not present
echo "Installing MongoDB..."
npm install mongodb

# Setup client dependencies
echo "Setting up client..."
cd client
npm install
cd ..

# Setup server dependencies  
echo "Setting up server..."
cd server
npm install
cd ..

# Setup AI service dependencies
echo "Setting up AI service..."
cd ai-service
pip install -r requirements.txt
cd ..

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure MongoDB is running"
echo "2. Install and start Ollama: https://ollama.ai"
echo "3. Pull a model: ollama pull mistral"
echo "4. Start each service in separate terminals"
echo ""
echo "Services:"
echo "- Client: cd client && npm start (port 3000)"
echo "- Server: cd server && npm run dev (port 5000)"  
echo "- AI Service: cd ai-service && uvicorn main:app --reload --port 8000"
