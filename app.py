from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# -------------------------
# Home Page
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# Ask AI
# -------------------------
@app.route("/ask", methods=["POST"])
def ask():

    try:
        data = request.get_json()

        question = data.get("question", "")
        subject = data.get("subject", "General")

        if not question.strip():
            return jsonify({
                "answer": "Please enter a question."
            })

        prompt = f"""
You are an AI Study Assistant.

Subject: {subject}

Student Question:
{question}

Give a clear, simple and accurate answer.

Explain the concept in an easy way suitable for a college student.

Use examples when helpful.

Do not make the answer unnecessarily complicated.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return jsonify({
            "answer": response.text
        })

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "answer": "Sorry, something went wrong. Please try again."
        })


# -------------------------
# Study Summary
# -------------------------
@app.route("/summary", methods=["POST"])
def summary():

    try:
        data = request.get_json()

        question = data.get("question", "")
        subject = data.get("subject", "General")

        if not question.strip():
            return jsonify({
                "answer": "Please enter a topic first."
            })

        prompt = f"""
You are an AI Study Assistant.

Subject: {subject}

Topic:
{question}

Create short and useful study notes for a college student.

Format:

📌 Topic

📝 Definition

🔑 Key Points

💡 Example

📚 Quick Revision

Keep the explanation simple, clear and exam-friendly.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return jsonify({
            "answer": response.text
        })

    except Exception as e:

        print("Summary Error:", e)

        return jsonify({
            "answer": "Unable to generate summary. Please try again."
        })


# -------------------------
# MCQ Generator
# -------------------------
@app.route("/mcq", methods=["POST"])
def mcq():

    try:
        data = request.get_json()

        question = data.get("question", "")
        subject = data.get("subject", "General")

        if not question.strip():
            return jsonify({
                "answer": "Please enter a topic first."
            })

        prompt = f"""
You are an AI Study Assistant.

Subject: {subject}

Topic:
{question}

Generate 5 multiple-choice questions for a college student.

For each question provide:

1. Question
A) Option
B) Option
C) Option
D) Option

Correct Answer: clearly mention the correct option.

Keep the questions educational, clear and suitable for exam preparation.

Do not make them unnecessarily difficult.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return jsonify({
            "answer": response.text
        })

    except Exception as e:

        print("MCQ Error:", e)

        return jsonify({
            "answer": "Unable to generate MCQs. Please try again."
        })


# -------------------------
# Run Application
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)