# ✉️ AI Email Prioritizer Agent

A smart inbox that auto-buckets mail into **Urgent**, **Read Later**, or **Ignore** and lets you correct the AI in real-time.

## 🚀 Demo
[Live on Streamlit Cloud](https://YOUR-DEPLOYED-URL)

## Features
| ✅ | Description |
|----|-------------|
| Auto-classify inbox | Zero-shot model (BART-MNLI) running on CPU |
| Real-time feedback  | “Reclassify” instantly updates the view & stores the label |
| CSV export          | Download whichever bucket you’re looking at |
| Privacy-first demo  | Ships with dummy US-centric emails; Gmail OAuth stubbed until verified |

## Quick Start (local)
```bash
git clone https://github.com/YOUR-USER/email-prioritizer-agent
cd email-prioritizer-agent
python -m venv env && source env/bin/activate
pip install -r requirements.txt
streamlit run app.py
