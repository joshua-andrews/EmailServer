import email
from email import policy
import sys

def test_email_parsing():
    raw_email = """Subject: Test Email
From: sender@example.com
To: recipient@example.com
Content-Type: multipart/alternative; boundary="boundary"

--boundary
Content-Type: text/plain

This is a plain text body.

--boundary
Content-Type: text/html

<html><body><p>This is an HTML body.</p></body></html>

--boundary--
"""
    msg = email.message_from_string(raw_email, policy=policy.default)
    
    print("Testing get_body() logic...")
    try:
        body = " (No Body) "
        body_part = msg.get_body(preferencelist=('plain', 'html'))
        if body_part:
            body = body_part.get_content()
        print(f"Successfully extracted body: {body.strip()}")
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_email_parsing()
