#!/bin/bash

echo "🚀 Setting up HoneyTrap with React Frontend..."

# Setup backend
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Setup frontend
echo "⚛️ Setting up React frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "🔧 To run the application:"
echo "1. Start backend: cd backend && python server.py"
echo "2. Start frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Access the dashboard at: http://localhost:3000"