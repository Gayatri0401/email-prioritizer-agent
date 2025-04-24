# ✉️ AI Email Prioritizer Agent

This is a smart email assistant that connects to Gmail and classifies emails as **Urgent 🔴**, **Read Later 🟡**, or **Promo 🚫** — built specifically for job seekers and recruiters.

## 🚀 Features

- ✅ Connects securely to your Gmail
- ✅ Classifies emails using smart rules + machine learning
- ✅ Highlights interviews, application steps, technical rounds
- ✅ Filters out promo and newsletter noise
- ✅ Works 100% locally for free using open-source models

## 📦 Tech Used

- Python 3
- Gmail API (OAuth)
- Hugging Face Transformers
- PyTorch + Numpy
- Rule-based filtering + zero-shot classification

## 🧪 Example Output

📨 Subject: Interview at Google ✉️ Snippet: Your technical round is scheduled for Thursday... 🔖 Category: Urgent 🔴

📨 Subject: 50% off Flipkart Deals! ✉️ Snippet: Exclusive offer ends soon... 🔖 Category: Promo 🚫

📨 Subject: HDFC Credit Card Statement ✉️ Snippet: Your monthly bill is now available... 🔖 Category: Read Later 🟡


## 🛠️ Installation

```bash
git clone https://github.com/Gayatri0401/email-prioritizer-agent
cd email-prioritizer-agent
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

---
Created by [@Gayatri0401](https://github.com/Gayatri0401) 🚀