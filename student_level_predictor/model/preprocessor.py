# model/preprocessor.py

import re
import nltk

# ✅ Automatically download stopwords (first time only)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords

# ✅ Load English stopwords
stop_words = set(stopwords.words("english"))

def clean_text(text):
    """
    Cleans input text by:
    - Lowercasing
    - Removing non-alphabetic characters
    - Removing English stopwords
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    filtered = [word for word in words if word not in stop_words]
    return " ".join(filtered)
