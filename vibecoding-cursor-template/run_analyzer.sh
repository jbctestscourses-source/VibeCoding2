#!/bin/bash

# User Story Analyzer - Run Script
# This script runs the Streamlit application for user story analysis

echo "🚀 Starting User Story Analyzer..."
echo "📋 This tool helps analyze user stories with Gemini AI"
echo ""

# Check if we're in the right directory
if [ ! -f "user_story_analyzer.py" ]; then
    echo "❌ Error: user_story_analyzer.py not found in current directory"
    echo "Please run this script from the vibecoding-cursor-template directory"
    exit 1
fi

# Check if .streamlit/secrets.toml exists and has a valid API key
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "❌ Error: .streamlit/secrets.toml not found"
    echo "Please create this file with your Gemini API key"
    exit 1
fi

# Run the Streamlit app
echo "🌐 Opening User Story Analyzer in your browser..."
echo "📍 URL: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 -m streamlit run user_story_analyzer.py --server.port 8501
