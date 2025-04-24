from gmail_auth import get_gmail_service
from email_reader import get_latest_emails
from classifier import classify_email

# Step 1: Connect to Gmail
service = get_gmail_service()

# Step 2: Fetch latest emails
emails = get_latest_emails(service)

# Step 3: Loop through and classify them
print("📬 Classifying Your Latest Emails:\n")

for i, email in enumerate(emails, 1):
    subject = email['subject']
    snippet = email['snippet']
    sender = email.get('from')

    category = classify_email(subject, snippet, sender)
    print(f"{i}. 📨 Subject: {subject}")
    print(f"   ✉️ Snippet: {snippet}")
    print(f"   👤 From: {sender}")
    print(f"   🔖 Category: {category}\n")