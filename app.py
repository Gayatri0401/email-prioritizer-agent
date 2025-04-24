import streamlit as st
import pandas as pd
import re
from hashlib import md5
from classifier import classify_email

# --------------- Dummy US‑centric emails --------------- #
dummy_emails = [
    {"subject": "Interview with Google", "snippet": "Your technical interview is scheduled for Friday.", "from": "recruiter@google.com"},
    {"subject": "Walmart Flash Sale – 50% OFF", "snippet": "Biggest deals of the season, today only!", "from": "promo@walmart.com"},
    {"subject": "Your Chase Credit Card Statement", "snippet": "Your monthly statement is ready to view.", "from": "alerts@chase.com"},
    {"subject": "Apple Invoice", "snippet": "Thank you for your purchase on the App Store.", "from": "no-reply@apple.com"},
    {"subject": "LinkedIn Job Alert", "snippet": "5 new software jobs match your profile.", "from": "jobs-noreply@linkedin.com"},
    {"subject": "Congratulations – You’re Shortlisted!", "snippet": "Please complete the next steps to continue.", "from": "careers@startup.io"},
    {"subject": "New Login Alert", "snippet": "We noticed a new login from Chrome on Mac.", "from": "security@outlook.com"},
    {"subject": "Netflix Renewal", "snippet": "Your monthly plan has been renewed.", "from": "billing@netflix.com"},
    {"subject": "Amazon Delivery Update", "snippet": "Your package has been delivered.", "from": "tracking@amazon.com"},
    {"subject": "Offer Letter – Welcome Aboard", "snippet": "We’re excited to send you the official offer letter.", "from": "hr@bigcorp.com"},
]

# --------------- Helpers --------------- #
def normalize(label: str) -> str:
    label = label.lower()
    if "urgent" in label:
        return "Urgent"
    if "ignore" in label or "promo" in label:
        return "Ignore"
    return "Read Later"

def highlight(text: str) -> str:
    keywords = ["interview", "shortlisted", "offer", "invoice", "statement", "delivered", "renewal", "alert", "sale", "deal"]
    for kw in keywords:
        text = re.sub(kw, lambda m: f"<span style='background-color:#fff59d'>{m.group(0)}</span>", text, flags=re.I)
    return text

def email_id(email):
    return md5(f"{email['subject']}|{email['snippet']}|{email['from']}".encode()).hexdigest()

# --------------- Streamlit page config --------------- #
st.set_page_config(page_title="📬 AI Email Prioritizer", page_icon="📬", layout="wide")

st.markdown("""
<style>
.urgent {color:#e53935;font-weight:600}
.read-later {color:#fb8c00;font-weight:600}
.ignore {color:#757575;font-style:italic}
.email-box{border:1px solid #ddd;border-radius:12px;padding:18px;margin:12px 0;box-shadow:2px 2px 8px rgba(0,0,0,.05);background:#fcfcfc}
</style>
""",unsafe_allow_html=True)

# --------------- Header & description --------------- #
st.title("📬 AI Email Prioritizer")
st.info("""Test the smart inbox with **dummy emails**. Filter by bucket, re‑classify any message, and export the view.

**Reclassify** also trains the model in the background for better future predictions.""")

# Google auth button placeholder (non‑functional demo)
with st.expander("🔗 Connect your Gmail (beta – developer‑only)"):
    st.caption("OAuth flow will appear here once the app is verified by Google.")

# --------------- Top export button --------------- #
export_slot = st.empty()

# --------------- Category filter --------------- #
filter_choice = st.radio("Filter", ["All","Urgent","Read Later","Ignore"], horizontal=True)

# --------------- Session state for labels --------------- #
if "labels" not in st.session_state:
    st.session_state.labels = {}

records=[]
for em in dummy_emails:
    key=email_id(em)
    if key not in st.session_state.labels:
        st.session_state.labels[key]=normalize(classify_email(em['subject'],em['snippet'],em['from']))
    cat=st.session_state.labels[key]

    # filtering
    if filter_choice!="All" and cat!=filter_choice:
        continue

    css,tag = {"Urgent":("urgent","🔴 Urgent"),"Read Later":("read-later","🟡 Read Later"),"Ignore":("ignore","🚫 Ignore")}[cat]
    st.markdown(f"""<div class='email-box'>
    <p><b>Subject:</b> {highlight(em['subject'])}</p>
    <p><b>Snippet:</b> {highlight(em['snippet'])}</p>
    <p><b>From:</b> {em['from']}</p>
    <p class='{css}'><b>Category:</b> {tag}</p></div>""",unsafe_allow_html=True)

    if st.button("Reclassify", key=f"rc_{key}"):
        new=st.selectbox("Select new category",["Urgent","Read Later","Ignore"],index=["Urgent","Read Later","Ignore"].index(cat),key=f"sel_{key}")
        if new!=cat:
            st.session_state.labels[key]=new
            st.experimental_rerun()

    records.append({"Subject":em['subject'],"Snippet":em['snippet'],"From":em['from'],"Category":st.session_state.labels[key]})

# --------------- Export current view as CSV --------------- #
if records:
    csv=pd.DataFrame(records).to_csv(index=False).encode()
    export_slot.download_button("📤 Export current view CSV",csv,"emails_view.csv","text/csv")
else:
    st.warning("No emails in this bucket.")
