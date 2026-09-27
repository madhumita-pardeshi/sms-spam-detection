"""Train and save the SMS spam model from Dataset/SMSSpamCollection."""

import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "Dataset" / "SMSSpamCollection"


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> None:
    if not DATASET_PATH.is_file():
        raise SystemExit(f"Dataset not found: {DATASET_PATH}")

    data = pd.read_csv(
        DATASET_PATH,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8",
    )
    data["clean_message"] = data["message"].astype(str).map(clean_text)

    x_train, x_test, y_train, y_test = train_test_split(
        data["clean_message"],
        data["label"],
        test_size=0.2,
        random_state=42,
        stratify=data["label"],
    )
    vectorizer = TfidfVectorizer()
    x_train_tfidf = vectorizer.fit_transform(x_train)
    model = MultinomialNB()
    model.fit(x_train_tfidf, y_train)

    predictions = model.predict(vectorizer.transform(x_test))
    print(f"Messages: {len(data):,}")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")
    print(classification_report(y_test, predictions, target_names=["ham", "spam"]))

    joblib.dump(model, BASE_DIR / "spam_model.pkl")
    joblib.dump(vectorizer, BASE_DIR / "tfidf_vectorizer.pkl")
    print("Saved spam_model.pkl and tfidf_vectorizer.pkl")


if __name__ == "__main__":
    main()
