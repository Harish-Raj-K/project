# model/classifier.py

import os
import pickle
from model.preprocessor import clean_text

def predict_level(course, text):
    """
    Predicts student skill level (1-3) for the selected course.
    Loads the model and vectorizer dynamically.
    """
    base_path = os.path.dirname(__file__)
    
    model_path = os.path.join(base_path, f"model_{course}.pkl")
    vect_path = os.path.join(base_path, f"vectorizer_{course}.pkl")

    # Load model and vectorizer
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vect_path, "rb") as f:
        vectorizer = pickle.load(f)

    # Preprocess input and predict
    cleaned = clean_text(text)
    transformed = vectorizer.transform([cleaned])
    prediction = model.predict(transformed)[0]

    return int(prediction)
