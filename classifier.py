"""
Light-weight zero-shot classifier used by Streamlit app.
"""

import os
os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"   # skip vision deps

from transformers import pipeline

# one-time model load (cached after first run)
_zero_shot = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1,             # CPU
)

_LABELS = ["Urgent", "Read Later", "Ignore"]


def classify_email(subject: str, snippet: str, sender: str = "") -> str:
    """
    Return one of 'Urgent' | 'Read Later' | 'Ignore'.
    The sender field is concatenated to help the model (optional).
    """
    text = f"{subject}\n\n{snippet}\n\n{sender}"
    result = _zero_shot(text, candidate_labels=_LABELS)
    return result["labels"][0]      # highest-score label
