@echo off
cd /d "%~dp0"
echo ===== Shortfundly Internship Chatbot =====
if not exist .venv ( py -m venv .venv )
call .venv\Scripts\activate
pip install -q -r requirements.txt
if not exist .env (
  echo.
  set /p KEY=Paste your Gemini API key here and press Enter: 
  > .env echo GEMINI_API_KEY=%KEY%
  >> .env echo GEMINI_MODEL=gemini-2.5-flash
)
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"
python app.py
pause
