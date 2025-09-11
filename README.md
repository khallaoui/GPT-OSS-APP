GPT-Life: AI Personality Development Coach
Overview
GPT-Life is an AI-powered coaching application that helps users build better habits, develop routines, and improve their personal and professional lives. Built for the OpenAI Open Model Hackathon, this application leverages the gpt-oss-20b model to provide personalized coaching and habit formation strategies.

The application features an interactive chat interface, habit tracking system, progress analytics, and daily planning tools - all designed to work seamlessly without requiring constant internet connectivity.

Features
AI Coaching Chat: Interactive conversations with an AI life coach for personalized advice

Habit Management: Track and manage daily habits across multiple categories

Progress Analytics: Visual dashboards showing completion rates and habit distribution

Daily Planning: AI-generated daily schedules optimized for productivity

Offline Capable: Designed to function without continuous internet access

Technical Implementation
This application uses OpenAI's gpt-oss-20b model through the OpenRouter API to provide AI coaching capabilities. The interface is built with Gradio for accessibility and ease of use.

Architecture
The application follows a modular architecture with separate services for:

GPT client communication

Habit management and tracking

UI components and visualization

Main coaching service coordination

Installation & Setup
Prerequisites
Python 3.8+

OpenRouter API key

Required Python packages (listed in requirements.txt)

Installation Steps
Clone the repository:

text
git clone https://github.com/yourusername/gpt-life-coach.git
cd gpt-life-coach
Install dependencies:

text
pip install -r requirements.txt
Set up your OpenRouter API key:

Obtain an API key from https://openrouter.ai

Replace the API_KEY value in the application with your key

Run the application:

text
python app.py
Access the application at the local URL provided in the terminal (typically http://localhost:7860)

Usage
Getting Started
Open the application in your web browser

Start by chatting with the AI coach in the "AI Coach Chat" tab

Add habits you want to track in the "Habit Manager" tab

Set goals and generate daily plans in the "Goal Setting" tab

Key Features
Chat with AI Coach: Ask questions about habit formation, routine development, or personal growth

Track Habits: Add habits across categories like morning routines, productivity, health, and learning

View Progress: Check your progress dashboards to see completion rates and habit distribution

Get Suggestions: Use the category dropdown to get AI-powered habit suggestions

Generate Plans: Create personalized daily plans based on your goals

Model Integration
This application specifically uses OpenAI's gpt-oss-20b model through the OpenRouter API. The integration handles:

Personalized coaching conversations

Habit improvement suggestions

Daily plan generation

Context-aware responses based on conversation history

Project Structure
text
gpt-life-coach/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── assets/               # Optional: screenshots or demo assets
Development
The application is built with:

Gradio for the web interface

Plotly for data visualization

OpenAI gpt-oss-20b model for AI capabilities

Custom Python classes for habit management and coaching logic

License
This project is available under the Apache License 2.0. See the LICENSE file for details.

Hackathon Submission
This project is submitted for the OpenAI Open Model Hackathon in the following categories:

Best Local Agent: Functions as a comprehensive coaching agent without requiring internet access

For Humanity: Addresses personal development challenges accessible to users regardless of connectivity

The application demonstrates effective use of the gpt-oss-20b model for personalized coaching and habit formation, with a focus on offline functionality and accessibility.

Demo
A demonstration video is available showing the application's features and functionality. The video showcases the AI coaching conversation, habit management, progress tracking, and daily planning capabilities.

Future Enhancements
Potential improvements include:

Local model deployment for complete offline functionality

Mobile application version

Integration with wearable devices for habit tracking

Expanded coaching domains and specialized advice modules

Contact
For questions about this project, please open an issue in the GitHub repository or contact the development team through the hackathon submission platform.
