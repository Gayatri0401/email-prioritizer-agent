import streamlit as st
import pandas as pd
import re
from hashlib import md5
from classifier import classify_email

# ──────────────────────────────────────────────────────────────
# Dummy US-centric inbox (10 mails)
DUMMY_EMAILS = [
    {"subject": "Interview with Google",
     "snippet": "Your technical interview is scheduled for Friday.",
     "from": "recruiter@google.com"},
    {"subject": "Walmart Flash Sale – 50% OFF",
     "snippet": "Biggest deals of the season, today only!",
     "from": "promo@walmart.com"},
    {"subject": "Your Chase Card Statement",
     "snippet": "Your monthly statement is ready to view.",
     "from": "alerts@chase.com"},
    {"subject": "Apple Invoice",
     "snippet": "Thank you for your App Store purchase.",
     "from": "no-reply@apple.com"},
    {"subject": "LinkedIn Job Alert",
     "snippet": "5 new software jobs match your profile.",
     "from": "jobs@linkedin.com"},
    {"subject": "Congratulations – You’re Shortlisted!",
     "snippet": "Please complete the next steps to continue.",
     "from": "careers@startup.io"},
    {"subject": "New Login Alert",
     "snippet": "We noticed a new login from Chrome on Mac.",
     "from": "security@outlook.com"},
    {"subject": "Netflix Renewal",
     "snippet": "Your monthly plan has been renewed.",
     "from": "billing@netflix.com"},
    {"subject": "Amazon Delivery Update",
     "snippet": "Your package has been delivered.",
     "from": "tracking@amazon.com"},
    {"subject": "Offer Letter – Welcome Aboard",
     "snippet": "We’re excited to send you the official offer letter.",
     "from": "hr@bigcorp.com"},
]

# ──────────────────────────────────────────────────────────────
# Utility helpers
KEYWORDS = [
    "interview", "shortlisted", "offer", "invoice", "statement",
    "delivered", "renewal", "alert", "sale", "deal",
]


def highlight(text: str) -> str:
    """Yellow-highlight key words inside text."""
    for kw in KEYWORDS:
        text = re.sub(
            kw, lambda m: f"<span style='background:#fffd8c'>{m.group(0)}</span>",
            text, flags=re.I)
    return text


def email_id(email: dict) -> str:
    """Stable hash used as session-state key."""
    raw = f"{email['subject']}|{email['snippet']}|{email['from']}"
    return md5(raw.encode()).hexdigest()


# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="📬 AI Email Prioritizer",
                   page_icon="📬", layout="wide")

# --- Global CSS (grey sidebar / white content) ----------------
st.markdown(
    """
    <style>
    /* grey sidebar */
    section[data-testid="stSidebar"] > div:first-child {
        background-color:#f7f7f7;
    }
    .urgent {color:#e53935;font-weight:600}
    .read-later {color:#fb8c00;font-weight:600}
    .ignore {color:#757575;font-style:italic}
    .email-box{
        border:1px solid #ddd;border-radius:10px;padding:16px;
        margin:14px 0;background:#ffffff;box-shadow:1px 1px 6px rgba(0,0,0,.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar description ───────────────────────────────────────
with st.sidebar:
    st.header("🔍 What this demo shows")
    st.write(
        """
        • **Bucket your inbox** into Urgent, Read Later, or Ignore  
        • **Re-classify** any mail — the model learns in-session  
        • **Export** the current view to CSV  
        
        *Uses dummy emails for privacy. Gmail OAuth coming once the app is
        verified.*
        """
    )

# ── Header + Export placeholder ───────────────────────────────
st.title("📬 AI Email Prioritizer")
export_area = st.empty()           # filled after table built

# ── Category filter ───────────────────────────────────────────
bucket = st.radio(
    "Filter view:", ["All", "Urgent", "Read Later", "Ignore"],
    horizontal=True)

# ── Session state to persist user labels ──────────────────────
if "labels" not in st.session_state:
    st.session_state.labels = {}

records = []
for email in DUMMY_EMAILS:
    key = email_id(email)

    # initial label or cached
    label = st.session_state.labels.get(key)
    if label is None:
        label = classify_email(email["subject"], email["snippet"], email["from"])
        label = "Ignore" if "Promo" in label else label   # normalize
        st.session_state.labels[key] = label

    # filter logic
    if bucket != "All" and label != bucket:
        continue

    css, tag = {
        "Urgent": ("urgent", "🔴 Urgent"),
        "Read Later": ("read-later", "🟡 Read Later"),
        "Ignore": ("ignore", "🚫 Ignore"),
    }[label]

    # UI card
    st.markdown(
        f"""
        <div class='email-box'>
          <p><b>Subject:</b> {highlight(email['subject'])}</p>
          <p><b>Snippet:</b> {highlight(email['snippet'])}</p>
          <p><b>From:</b> {email['from']}</p>
          <p class='{css}'><b>Category:</b> {tag}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Re-classify
    if st.button("Reclassify", key=f"btn_{key}"):
        new = st.selectbox(
            "Choose new bucket",
            ["Urgent", "Read Later", "Ignore"],
            index=["Urgent", "Read Later", "Ignore"].index(label),
            key=f"sel_{key}",
        )
        if new != label:
            st.session_state.labels[key] = new
            st.experimental_rerun()

    records.append({
        "Subject": email["subject"],
        "Snippet": email["snippet"],
        "From": email["from"],
        "Category": st.session_state.labels[key],
    })

# ── Export view ───────────────────────────────────────────────
if records:
    csv = pd.DataFrame(records).to_csv(index=False).encode()
    export_area.download_button(
        "📤 Export current view (CSV)",
        csv,
        "emails_view.csv",
        "text/csv")
else:
    export_area.info("No emails in this bucket.")
