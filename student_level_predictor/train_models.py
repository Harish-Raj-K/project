# train_models.py

import sys
import os

# Ensure the model module is accessible
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from model.preprocessor import clean_text


# Define your available courses and their dataset filenames
courses = {
    "python": "data/python_dataset.csv",
    "genai": "data/genai_dataset.csv",
    "datascience": "data/datascience_dataset.csv",
    "fullstack": "data/fullstack_dataset.csv"
}

# Path to the model directory
model_dir = os.path.join(os.path.dirname(__file__), "model")

for course_key, dataset_path in courses.items():
    print(f"\n📚 Training model for: {course_key.upper()}")

    # Load dataset
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"❌ File not found: {dataset_path}")
        continue

    # Ensure required columns are present
    if "response" not in df.columns or "level" not in df.columns:
        print(f"⚠️ Skipping {course_key}: Missing 'response' or 'level' column in CSV")
        continue

    # Preprocess and train
    df["cleaned"] = df["response"].apply(clean_text)
    X = df["cleaned"]
    y = df["level"]

    vectorizer = TfidfVectorizer()
    X_vect = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=200)
    model.fit(X_vect, y)

    # Save model and vectorizer
    model_path = os.path.join(model_dir, f"model_{course_key}.pkl")
    vect_path = os.path.join(model_dir, f"vectorizer_{course_key}.pkl")

    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(vect_path, "wb") as f:
        pickle.dump(vectorizer, f)

    print(f"✅ Saved model and vectorizer for {course_key}!")

print("\n🎉 All models trained successfully.")
