
# Shortfundly Internship Assistant

An AI-powered chatbot designed to help students understand and complete their internship tasks step by step.

## Features

- Explains internship tasks in simple steps
- Supports English, Tamil, and Hindi responses
- Helps review task requirements and submitted code
- Provides guidance on missing modules and corrections
- Includes a feedback email form for review communication
- Built using Python and Flask with Gemini API integration

## Technologies Used

- Python
- Flask
- Google Gemini API
- HTML, CSS, JavaScript
- SMTP Email Integration

## Project Structure

- `app.py` - Flask application and chatbot logic
- `templates/` - Website HTML templates
- `static/` - CSS and JavaScript files
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template

## Setup Instructions

1. Install Python.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Configure your Gemini API key and other required settings in a local `.env` file.
6. Start the application:

   `python app.py`

7. Open `http://127.0.0.1:5000` in your browser.

## Environment Variables

Configure `GEMINI_API_KEY`, `GEMINI_MODEL`, and the required email settings in your local environment. Never upload actual API keys, passwords, or other secrets to GitHub.

## Author

Abhinaya S
