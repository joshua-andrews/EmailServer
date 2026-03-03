import sys
import requests
import email
from email import policy
import logging

# Configuration
WEBHOOK_URL = "https://web-production-48500.up.railway.app/webhook"
LOG_FILE = "/var/log/email-webhook.log"

# Force logging to file, disregard potential permission errors by using try/except if needed? 
# Using a safer location or ensuring permissions. /var/log/ usually requires root.
# Maddy runs as 'maddy' user? 
# If maddy runs as 'maddy', it can't write to /var/log/email-webhook.log unless created/owned by maddy.
# AND it might not have network access? 
# But let's fix the script logic first.

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def main():
    try:
        # Args: script.py <sender> <recipients> <msg_id>
        # Check lengths to avoid IndexError
        sender = sys.argv[1] if len(sys.argv) > 1 else "unknown"
        recipients = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        msg_id = sys.argv[3] if len(sys.argv) > 3 else "unknown"

        # Read body from stdin
        raw_content = sys.stdin.read()
        
        msg = email.message_from_string(raw_content, policy=policy.default)
        body = "No text body"
        try:
            body_part = msg.get_body(preferencelist=('plain', 'html'))
            if body_part:
                body = body_part.get_content()
        except Exception:
            pass

        payload = {
            "sender": sender,
            "recipient": recipients,
            "subject": msg['subject'] or "(No Subject)",
            "body": body,
            "message_id": msg_id
        }
        
        logging.info(f"Forwarding {msg_id}")
        
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception as req_err:
            logging.error(f"Webhook connection failed: {req_err}")

    except Exception as e:
        # Catch ALL errors to prevent exit code 1
        logging.error(f"Script Error: {e}")
    
    # CRITICAL: Always exit 0 to tell Maddy "Success" (even if webhook failed)
    # This prevents the email from bouncing.
    sys.exit(0)

if __name__ == "__main__":
    main()
