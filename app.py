import streamlit as st
import pandas as pd
from classifier import classify_email

# Dummy email dataset (replaceable with real or uploaded ones)
dummy_emails = [
    {"subject": "Interview with Google", "snippet": "Your technical round is scheduled for Friday.", "from": "recruiter@google.com"},
    {"subject": "50% Off Flipkart Deals", "snippet": "Big Billion Days are here!", "from": "promo@flipkart.com"},
    {"subject": "Your HDFC Credit Card Statement", "snippet": "Your statement for this month is ready.", "from": "alerts@hdfc.com"},
    {"subject": "Offer from Amazon", "snippet": "Save up to 60% today only!", "from": "promo@amazon.com"},
    {"subject": "LinkedIn Job Alert", "snippet": "5 new jobs match your profile.", "from": "jobs@linkedin.com"},
    {"subject": "Resume Shortlisted", "snippet": "You've been shortlisted for next steps.", "from": "hr@startup.com"},
    {"subject": "New Login to Your Account", "snippet": "We noticed a new login.", "from": "security@xyz.com"},
    {"subject": "Netflix Subscription Renewal", "snippet": "Your monthly plan has been renewed.", "from": "billing@netflix.com"},
    {"subject": "Exclusive Invite to Webinar", "snippet": "Join us this weekend.", "from": "events@saascompany.com"},
    {"subject": "Apple Invoice", "snippet": "Your receipt for Apple Music.", "from": "billing@apple.com"},
    {"subject": "Team Standup Notes", "snippet": "Here are today's highlights.", "from": "teammate@company.com"},
    {"subject": "Free Udemy Course!", "snippet": "Claim your 100% free learning access.", "from": "deals@udemy.com"},
    {"subject": "Congratulations! You’re shortlisted", "snippet": "Schedule your interview now.", "from": "careers@unicorn.com"},
    {"subject": "Amazon Delivered", "snippet": "Your package was delivered.", "from": "tracking@amazon.com"},
    {"subject": "Paytm Cashback Received", "snippet": "₹50 added to your wallet.", "from": "rewards@paytm.com"},
    {"subject": "Reminder: Doctor's Appointment", "snippet": "This is your confirmation.", "from": "noreply@clinic.com"},
    {"subject": "Offer Letter", "snippet": "We’re excited to welcome you.", "from": "hr@company.com"},
    {"subject": "Google Calendar Invite", "snippet": "You’ve been invited.", "from": "noreply@calendar.google.com"},
    {"subject": "Spotify Premium Update", "snippet": "New playlist just dropped!", "from": "music@spotify.com"},
    {"subject": "Important Account Alert", "snippet": "Action needed now.", "from": "support@bank.com"},
]

st.set_page_config(page_title="📬 AI Email Prioritizer", page_icon="📬", layout="wide")

st.markdown("""
    <style>
    .urgent {color: red; font-weight: bold;}
    .read-later {color: orange; font-weight: bold;}
    .promo {color: grey; font-style: italic;}
    .email-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        background-color: #fdfdfd;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📬 AI Email Prioritizer")

with st.sidebar:
    st.markdown("""
    ### 🔐 How This Works
    To protect privacy and simplify sharing, this demo uses 20 **dummy emails**.

    You can still try the full experience:
    - See how the model classifies emails
    - Reclassify if needed
    - Export to CSV

    👉 Want to use **your Gmail** instead?
    Click the button below to authorize and classify your actual inbox (developer-only feature).
    """)
    st.button("🔗 Connect Gmail (for verified users)")

filter_category = st.radio(
    "🔎 Filter Emails by Category:",
    ("All", "Urgent", "Read Later", "Promo"),
    horizontal=True
)

user_reclassifications = []
all_data = []

with st.spinner("Classifying dummy emails..."):
    for idx, email in enumerate(dummy_emails):
        subject = email.get("subject", "(No Subject)")
        snippet = email.get("snippet", "")
        sender = email.get("from", "Unknown")
        category = classify_email(subject, snippet, sender)

        if filter_category != "All" and category != filter_category:
            continue

        tag_class = {
            "Urgent": "urgent",
            "Promo": "promo",
            "Read Later": "read-later"
        }.get(category, "")

        tag_text = {
            "Urgent": "🔴 Urgent",
            "Promo": "🚫 Promo",
            "Read Later": "🟡 Read Later"
        }.get(category, category)

        with st.container():
            st.markdown(f"""
                <div class='email-box'>
                    <p><strong>Subject:</strong> {subject}</p>
                    <p><strong>Snippet:</strong> {snippet}</p>
                    <p><strong>From:</strong> {sender}</p>
                    <p class='{tag_class}'><strong>Category:</strong> {tag_text}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"✏️ Reclassify Email #{idx+1}", key=f"reclass_button_{idx}"):
                new_category = st.radio(
                    "Choose new category:",
                    ["Urgent", "Read Later", "Promo"],
                    key=f"reclass_radio_{idx}"
                )
                if new_category != category:
                    user_reclassifications.append({
                        "subject": subject,
                        "snippet": snippet,
                        "from": sender,
                        "original": category,
                        "reclassified": new_category
                    })

        all_data.append({
            "Subject": subject,
            "Snippet": snippet,
            "From": sender,
            "Category": category
        })

if user_reclassifications:
    st.markdown("### ✍️ User Reclassifications")
    for change in user_reclassifications:
        st.write(f"➡️ **{change['subject']}** changed from *{change['original']}* to *{change['reclassified']}*")

if all_data:
    df = pd.DataFrame(all_data)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📤 Export All Emails to CSV",
        data=csv,
        file_name="classified_emails.csv",
        mime="text/csv"
    )
