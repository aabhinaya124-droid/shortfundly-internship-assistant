
import os
import time
import smtplib
from email.message import EmailMessage

import requests
from flask import Flask, render_template, request, jsonify, flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY", "change-this-for-local-demo"
)


# ---------------- GEMINI AI ----------------

def ask_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")

    if api_key in ("your_gemini_api_key", "YOUR_GEMINI_API_KEY_HERE"):
        api_key = ""

    if not api_key:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )

    last_error = "AI service unavailable."

    for attempt in range(4):
        try:
            response = requests.post(
                url,
                json={
                    "contents": [
                        {"parts": [{"text": prompt}]}
                    ],
                    "generationConfig": {"temperature": 0.3},
                },
                timeout=40,
            )

            if response.status_code in (429, 500, 502, 503, 504):
                last_error = (
                    f"AI service busy ({response.status_code}). "
                    "Please try again in a minute."
                )
                time.sleep(2 * (attempt + 1))
                continue

            if response.status_code != 200:
                try:
                    detail = response.json().get(
                        "error", {}
                    ).get("message", response.text[:200])
                except Exception:
                    detail = response.text[:200]

                return f"AI service error {response.status_code}: {detail}"

            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as exc:
            last_error = (
                f"AI service unavailable ({type(exc).__name__}: {exc})."
            )
            time.sleep(2)

    return last_error


# ---------------- CHATBOT REPLY ----------------

def bot_reply(message, language="English"):

    prompt = f"""You are Shortfundly Internship Assistant.

IMPORTANT LANGUAGE RULE:
- Reply ONLY in {language}.
- If the selected language is Tamil, write the entire answer in
  natural Tamil using Tamil script.
- If the selected language is Hindi, write the entire answer in Hindi.
- If the selected language is English, reply in English.
- Do not switch to English except for technical terms or code
  when necessary.
- Keep explanations clear, friendly, and beginner-friendly.

You help students understand internship tasks, break tasks into steps,
review pasted work against requirements, identify missing modules,
suggest corrections, and draft feedback emails.

Do not claim to inspect a GitHub link unless its contents are pasted
into the chat.
Do not claim an email was sent unless the email function confirms it.

User message: {message}

Answer in {language} only."""

    answer = ask_gemini(prompt)

    if answer:
        return answer

    # Localized responses when the Gemini API key is unavailable.
    if language == "Tamil":
        return (
            "வணக்கம்! நான் உங்கள் Shortfundly Internship Assistant.\n\n"
            "உங்கள் internship task-ஐ படிப்படியாக விளக்க உதவுகிறேன்.\n"
            "1. உங்கள் task requirements-ஐ அனுப்புங்கள்.\n"
            "2. நீங்கள் செய்த வேலை அல்லது code-ஐ பகிருங்கள்.\n"
            "3. அதைச் சரிபார்த்து அடுத்த படிகளை விளக்குகிறேன்.\n\n"
            "குறிப்பு: இப்போது Demo mode செயல்படுகிறது. "
            "AI பதில்களுக்கு GEMINI_API_KEY அமைக்கப்பட வேண்டும்."
        )

    if language == "Hindi":
        return (
            "नमस्ते! मैं आपका Shortfundly Internship Assistant हूँ।\n\n"
            "मैं आपके internship task को चरण-दर-चरण समझाने में मदद करूँगा।\n"
            "1. अपने task requirements भेजें।\n"
            "2. अपना काम या code साझा करें।\n"
            "3. मैं आपको अगले चरण समझाऊँगा।\n\n"
            "अभी Demo mode सक्रिय है। AI उत्तरों के लिए "
            "GEMINI_API_KEY सेट करना आवश्यक है।"
        )

    return (
        "Welcome! I can explain your internship task step by step.\n\n"
        "1. Paste the original task requirements.\n"
        "2. Share your completed work or code.\n"
        "3. I will help you review it and plan the next steps.\n\n"
        "Demo mode is active because GEMINI_API_KEY is not configured."
    )


# ---------------- EMAIL FUNCTION ----------------

def send_email(to_address, subject, body):
    host = os.getenv("SMTP_HOST", "").strip()
    user = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    port = int(os.getenv("SMTP_PORT", "587"))
    sender = os.getenv("SMTP_FROM", user).strip()

    if not (host and user and password and sender and to_address):
        return (
            False,
            "Email not sent: configure SMTP_HOST, SMTP_USER, "
            "SMTP_PASSWORD, and SMTP_FROM."
        )

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_address
        msg.set_content(body)

        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)

        return True, "Email sent successfully."

    except Exception as exc:
        return False, f"Email sending failed: {type(exc).__name__}: {exc}"


# ---------------- WEBSITE ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify({
        "gemini_key_loaded": bool(
            os.getenv("GEMINI_API_KEY", "").strip()
        ),
        "folder": BASE_DIR,
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    message = (data.get("message") or "").strip()
    language = str(data.get("language", "English")).strip()

    # Standardize the selected language.
    language_map = {
        "Tamil": "Tamil",
        "தமிழ்": "Tamil",
        "Hindi": "Hindi",
        "हिन्दी": "Hindi",
        "English": "English",
    }

    language = language_map.get(language, language)

    if not message:
        return jsonify({"reply": "Please type a message first."}), 400

    reply = bot_reply(message, language)

    return jsonify({"reply": reply})


@app.route("/review-email", methods=["GET", "POST"])
def review_email():
    if request.method == "POST":
        candidate = request.form.get("candidate", "").strip()
        email = request.form.get("email", "").strip()
        feedback = request.form.get("feedback", "").strip()
        review_date = request.form.get("review_date", "").strip()
        review_time = request.form.get("review_time", "").strip()
        meeting_link = request.form.get("meeting_link", "").strip()

        if not all([
            candidate,
            email,
            feedback,
            review_date,
            review_time,
            meeting_link,
        ]):
            flash("Please fill every field.", "error")

        else:
            body = (
                f"Hello {candidate},\n\n"
                f"Feedback:\n{feedback}\n\n"
                f"Next review details:\n"
                f"Date: {review_date}\n"
                f"Time: {review_time}\n"
                f"Meeting link: {meeting_link}\n\n"
                "Regards,\n"
                "Shortfundly Internship Assistant"
            )

            ok, msg = send_email(
                email,
                "Internship task feedback and next review",
                body,
            )

            flash(msg, "success" if ok else "error")

    return render_template("review_email.html")


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=int(os.getenv("PORT", "5000")),
    )
