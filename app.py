import streamlit as st
import pandas as pd
import re
from hashlib import md5
from classifier import classify_email

# ----------------------- Dummy US‑centric email set ----------------------- #
dummy_emails = [
    {"subject": "Interview with Google", "snippet": "Your technical interview is scheduled for Friday.", "from": "recruiter@google.com"},
    {"subject": "Walmart Flash Sale – 50% OFF", "snippet": "Biggest deals of the season, today only!", "from": "promo@walmart.com"},
    {"subject": "Your Chase Credit Card Statement", "snippet": "Your monthly statement is ready to view.", "from": "alerts@chase.com"},
    {"subject": "Apple Invoice", "snippet": "Thank you for your purchase on the App Store.", "from": "no‑reply@apple.com"},
    {"subject": "LinkedIn Job Alert", "snippet": "5 new software jobs match your profile.", "from": "jobs-noreply@linkedin.com"},
    {"subject": "Congratulations – You’re Shortlisted!", "snippet": "Please complete the next steps to continue.", "from": "careers@startup.io"},
    {"subject": "New Login Alert", "snippet": "We noticed a new login from Chrome on Mac.", "from": "security@outlook.com"},
    {"subject": "Netflix Subscription Renewal", "snippet": "Your monthly plan has been renewed.", "from": "billing@netflix.com"},
    {"subject": "Amazon Delivery Update", "snippet": "Your package has been delivered.", "from": "tracking@amazon.com"},
    {"subject": "Offer Letter – Welcome Aboard", "snippet": "We’re excited to send you the official offer letter.", "from": "hr@bigcorp.com"},
]

# ----------------------- Streamlit page config --------------------------- #
st.set_page_config(page_title="📬 AI Email Prioritizer", page_icon="📬", layout="wide")

# ----------------------- Utility functions ------------------------------- #

def highlight(text: str) -> str:
    """Highlight key hiring / promo words."""
    keywords = [
        "interview", "shortlisted", "offer", "invoice", "statement",
        "delivered", "renewal", "alert", "sale", "deal"
    ]
    def repl(match):
        return f"<span style='background-color:#fff59d'>{match.group(0)}</span>"
    for kw in keywords:
        text = re.sub(kw, repl, text, flags=re.IGNORECASE)
    return text

# Unique id for each email to track in session

def email_id(email):
    raw = f"{email['subject']}|{email['snippet']}|{email['from']}"
    return md5(raw.encode()).hexdigest()

# ----------------------- Sidebar description ----------------------------- #
with st.sidebar:
    st.markdown("""
    ### 🔐 Privacy‑First Demo
    This demo uses **dummy emails** so you can explore every feature safely.

    * Click **Filter** buttons to bucket emails.
    * Use **Reclassify** to teach the AI – your feedback is stored in‑memory.
    * Export the current view to CSV any time.

    _(Gmail connection for verified users only – no credentials are stored.)_
    """)

# ----------------------- Title & Export button --------------------------- #
st.title("📬 AI Email Prioritizer")

# Placeholder for export button – created after dataframe is ready
export_slot = st.empty()

# ----------------------- Category filter buttons ------------------------- #
col1, col2, col3, col4 = st.columns(4)
with col1:
    chosen_filter = st.radio("Filter", ["All", "Urgent", "Read Later", "Promo"], index=0, key="filter", horizontal=True)

# ----------------------- Session state for re‑labels --------------------- #
if "labels" not in st.session_state:
    st.session_state.labels = {}

# ----------------------- Classification loop ---------------------------- #
view_records = []
for idx, email in enumerate(dummy_emails):
    key = email_id(email)

    # Determine category (AI or user‑updated)
    category = st.session_state.labels.get(key)
    if category is None:
        category = classify_email(email["subject"], email["snippet"], email["from"])
        st.session_state.labels[key] = category  # cache initial label

    # Filter logic
    if chosen_filter != "All" and category != chosen_filter:
        continue

    # Build UI card
    tag_style = {
        "Urgent": ("urgent", "🔴 Urgent"),
        "Promo": ("promo", "🚫 Promo"),
        "Read Later": ("read-later", "🟡 Read Later"),
    }
    css_class, tag_text = tag_style.get(category, ("", category))

    st.markdown(f"""
        <div class='email-box'>
            <p><strong>Subject:</strong> {highlight(email['subject'])}</p>
            <p><strong>Snippet:</strong> {highlight(email['snippet'])}</p>
            <p><strong>From:</strong> {email['from']}</p>
            <p class='{css_class}'><strong>Category:</strong> {tag_text}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("✏️ Reclassify", key=f"reclass_{key}"):
        new_cat = st.selectbox("Select new category", ["Urgent", "Read Later", "Promo"], key=f"select_{key}")
        if new_cat != category:
            st.session_state.labels[key] = new_cat
            st.experimental_rerun()

    # Collect record for export
    view_records.append({
        "Subject": email["subject"],
        "Snippet": email["snippet"],
        "From": email["from"],
        "Category": st.session_state.labels[key]
    })

# ----------------------- Export current view ----------------------------- #
if view_records:
    df_view = pd.DataFrame(view_records)
    csv_bytes = df_view.to_csv(index=False).encode("utf-8")
    export_slot.download_button(
        label="📤 Export Displayed Emails as CSV",
        data=csv_bytes,
        file_name="emails_view.csv",
        mime="text/csv"
    )
else:
    st.info("No emails to display for this filter.")
