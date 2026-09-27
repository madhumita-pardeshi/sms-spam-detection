"""A small web interface for the SMS spam classifier."""

import os
import re
from pathlib import Path

import joblib
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # 16 KB is ample for an SMS.

MODEL_PATH = BASE_DIR / "spam_model.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"
missing_files = [path.name for path in (MODEL_PATH, VECTORIZER_PATH) if not path.is_file()]
if missing_files:
    names = " and ".join(missing_files)
    raise SystemExit(
        f"\nCannot start: {names} {('is' if len(missing_files) == 1 else 'are')} missing.\n"
        "Do not run app.py from inside the ZIP. Right-click the ZIP, choose 'Extract All', "
        "then run START_APP.bat from the extracted project folder.\n"
    )

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def clean_text(text: str) -> str:
    """Apply the same normalization used while training the model."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    result = None
    error = None

    if request.method == "POST":
        message = request.form.get("message", "")[:5000]
        if not message.strip():
            error = "Please enter a message to check."
        else:
            features = vectorizer.transform([clean_text(message)])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            result = {
                "label": "spam" if prediction == "spam" else "ham",
                "confidence": round(float(max(probabilities)) * 100, 1),
            }

    return render_template("index.html", message=message, result=result, error=error)


if __name__ == "__main__":
    import threading
    import webbrowser

    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
