# QUICK START (Windows)
1. Extract the zip.
2. Double-click START.bat
3. First time: paste your Gemini API key when asked. Browser opens automatically.
   (To change the key later: delete the .env file and run START.bat again.)

---

# Shortfundly Internship AI Chatbot

A chat-style Flask website prototype for:
- Explaining internship tasks in English, Tamil, or Hindi.
- Helping candidates understand requirements and request work reviews.
- A separate feedback email form including the next review date, time, and meeting link.

## Run on Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
$env:GEMINI_MODEL="gemini-2.5-flash"
python app.py
```
Open http://127.0.0.1:5000

Without `GEMINI_API_KEY`, the chatbot shows demo-mode guidance and does not generate real AI answers.
To send real emails, configure SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, and SMTP_FROM environment variables. For Gmail, use an App Password if available, not your normal password. Never commit API keys/passwords.

## Demo recording
Record opening the chatbot, selecting language, explaining a sample task, asking for a review, then using Feedback Email with a test address and review date/time/link. Only show successful email delivery if SMTP is configured and the app confirms success.

## Limitations
The chatbot does not automatically inspect private GitHub links or execute candidate code. Paste the relevant requirements and submission text for review. This is a prototype; production requires authentication, database storage, safe file handling, background jobs, and access controls.
