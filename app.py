import streamlit as st
import pandas as pd
from gmail_auth import get_gmail_service
from email_reader import get_latest_emails
from classifier import classify_email

st.set_page_config(page_title="📬 AI Email Prioritizer", page_icon="📬", layout="centered")

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
st.write("This smart assistant connects to Gmail and sorts your emails by importance.")

filter_category = st.radio(
    "🔎 Filter Emails by Category:",
    ("All", "Urgent", "Read Later", "Promo"),
    horizontal=True
)

if st.button("📥 Load and Classify Emails"):
    with st.spinner("Connecting to Gmail and classifying messages..."):
        service = get_gmail_service()
        emails = get_latest_emails(service)
        user_reclassifications = []
        all_data = []

        for idx, email in enumerate(emails):
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

        st.success("Done! All emails classified.")

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