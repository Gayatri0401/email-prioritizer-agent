import os
os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"   # <-- add this
from transformers import pipeline
import re
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_email(subject, snippet, sender=None):
    text = f"{subject} {snippet}".lower()

    promo_keywords = ["unsubscribe", "offer", "sale", "deal", "exclusive", "discount", "coupon", "promo", "newsletter"]
    promo_domains = ["@marketing", "@no-reply", "@noreply", "@offers", "@zomato", "@flipkart", "@amazon", "@nykaa"]

    job_keywords = [
        "technical round", "interview", "interview scheduled", "next steps", 
        "application received", "shortlisted", "recruiter", "job opportunity", 
        "take-home assignment", "coding round", "hr round", "offer letter", "please confirm availability"
    ]

    info_keywords = ["receipt", "payment", "transaction", "bank", "statement", "invoice", "bill"]
    article_keywords = ["newsletter", "blog", "update", "insights", "digest"]

    # Rule 1: Promo detection
    if any(kw in text for kw in promo_keywords) or (sender and any(domain in sender.lower() for domain in promo_domains)):
        return "Promo"

    # Rule 2: Job-related / Interview-related urgency
    if any(kw in text for kw in job_keywords):
        return "Urgent 🔴"

    # Rule 3: Read Later (payment info, articles)
    if any(kw in text for kw in info_keywords + article_keywords):
        return "Read Later 🟡"

    # Fallback: Use AI to guess if not clear
    labels = ["Urgent", "Read Later", "Promo"]
    result = classifier(text, candidate_labels=labels)
    return result["labels"][0] + " (AI)"
