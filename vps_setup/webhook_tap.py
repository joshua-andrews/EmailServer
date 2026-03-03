import sys
import requests
import email
from email import policy
import logging

# Configuration
WEBHOOK_URL = "https://web-production-48500.up.railway.app/webhook"
LOG_FILE = "/var/log/email-webhook.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def main():
    try:
        # Read args from Maddy: script.py <sender> <recipients> <msg_id>
        sender = sys.argv[1] if len(sys.argv) > 1 else "unknown"
        recipients = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        msg_id = sys.argv[3] if len(sys.argv) > 3 else "unknown"

        # Read body from STDIN
        raw_content = sys.stdin.read()
        
        # Parse Email
        msg = email.message_from_string(raw_content, policy=policy.default)
        subject = msg['subject'] or "(No Subject)"
        
        # Extract Body
        body = "No text body"
        try:
            body_part = msg.get_body(preferencelist=('plain', 'html'))
            if body_part:
                body = body_part.get_content()
        except Exception:
            pass

        # Send to Webhook
        payload = {
            "sender": sender,
            "recipient": recipients, 
            "subject": subject,
            "body": body,
            "message_id": msg_id
        }
        
        logging.info(f"Forwarding {msg_id}")
        
        # Fire and forget (almost) - 2s timeout
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=2)
        except Exception as e:
            logging.error(f"Webhook Failed: {e}")

    except Exception as e:
        logging.error(f"Critical Error: {e}")
        # Always exit 0 to not block email delivery
        sys.exit(0)

if __name__ == "__main__":
    main()
