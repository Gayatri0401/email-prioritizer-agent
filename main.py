from classifier import classify_email

subject = input("Subject: ")
snippet = input("Snippet: ")
cat = classify_email(subject, snippet)
print("→", cat)
