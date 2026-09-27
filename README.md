# TextShield — SMS Spam Detection

A responsive web app for checking SMS messages with a TF-IDF + Multinomial Naive Bayes classifier. It labels a message as **spam** or **ham** (likely legitimate) and shows the model confidence. The supplied trained model files are included, so you do not need to train the model to run the app.

> For educational use. Automated predictions may be wrong; do not treat a result as a safety guarantee.

## Windows quick start

1. In File Explorer, right-click `TextShield-SMS-Spam-Checker.zip` and choose **Extract All…**. Do not run `app.py` from inside the ZIP.
2. Open the extracted `TextShield-SMS-Spam-Checker` folder.
3. Double-click `START_APP.bat`. On first launch it creates a local Python environment and installs the requirements. This needs an internet connection.
4. Your browser opens the app at <http://127.0.0.1:5000>. Keep the terminal window open while using it; press **Ctrl+C** to stop the app.

If Python is not installed, install Python 3.12 or newer from <https://www.python.org/downloads/> and select **Add Python to PATH** during installation. If package installation fails, check your internet connection and run `START_APP.bat` again.

### Manual start

Use Python 3.12 or newer. Open PowerShell in the extracted project folder and run:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000>.

## Train the model again (optional)

The included model is ready to use. To retrain it from the included dataset, activate the environment, install requirements, then run:

```bash
python read_dataset.py
```

The script reports a held-out evaluation and replaces the two `.pkl` model files.

## Project files

```text
app.py                   Flask web app
templates/index.html     Responsive checker page
static/style.css         Page styling
spam_model.pkl           Trained Naive Bayes model
tfidf_vectorizer.pkl     Fitted TF-IDF vectorizer
Dataset/SMSSpamCollection SMS Spam Collection data
read_dataset.py          Reproducible model training script
requirements.txt         Python dependencies
START_APP.bat            Windows one-click local launcher
START_HERE.txt           Quick-start instructions
render.yaml              Optional Render deployment configuration
```

## Optional: deploy as a public website

To let other people use the app from one link, publish the project to GitHub and deploy it as a **Web Service** on Render. Configure the build command as `pip install -r requirements.txt` and the start command as `gunicorn app:app`. The public link is created by the hosting provider after deployment. You do not need to do this to run the project locally.

## Privacy

The app does not save message text to a database. Avoid entering sensitive content. A hosted version may have ordinary request metadata logged by its hosting provider.
