import sys
import smtplib
import requests
import email
from email.message import EmailMessage
from email.policy import default
import logging

WEBHOOK_URL = "https://web-production-48500.up.railway.app/webhook"
FORWARD_TO = "thankyoumr.a@gmail.com"
DEFAULT_FORWARD_FROM = "info@getcopyculture.com"
SMTP_SERVER = "127.0.0.1"
SMTP_PORT = 2525
WHITELIST = ["alerts@getcopyculture.com", "info@getcopyculture.com"]
LOG_FILE = "/tmp/email-webhook.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def main():
    try:
        sender = sys.argv[1] if len(sys.argv) > 1 else "unknown"
        recipients = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        msg_id = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        
        # Read raw content from stdin (simulated or real)
        raw_content = sys.stdin.read()
        
        original_msg = email.message_from_string(raw_content, policy=default)
        original_subject = original_msg['subject'] or "(No Subject)"
        
        body = "No text body"
        try:
            body_part = original_msg.get_body(preferencelist=('plain', 'html'))
            if body_part:
                body = body_part.get_content()
        except Exception:
            pass
            
        # Dynamic Sender Logic
        forward_from = DEFAULT_FORWARD_FROM
        
        # Safe lower() calls on strings
        recipients_lower = recipients.lower()
        
        for allowed in WHITELIST:
            if allowed in recipients_lower:
                forward_from = allowed
                break

        should_forward = any(allowed in recipients_lower for allowed in WHITELIST)
        
        if should_forward:
            try:
                forward_msg = EmailMessage()
                forward_msg['Subject'] = f"[Fwd] {original_subject}"
                forward_msg['From'] = forward_from
                forward_msg['To'] = FORWARD_TO
                forward_msg['Reply-To'] = sender
                
                # Manual concatenation for safety
                c = "----- Forwarded Message -----\n"
                c += f"From: {sender}\n"
                c += f"To: {recipients}\n"
                c += f"Subject: {original_subject}\n\n"
                c += f"{body}"
                
                forward_msg.set_content(c)
                try:
                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
                        s.send_message(forward_msg)
                        logging.info(f"Forwarded email from {sender} to {FORWARD_TO} as {forward_from}")
                except ConnectionRefusedError:
                     logging.error(f"Failed to connect to SMTP server at {SMTP_SERVER}:{SMTP_PORT}")
            except Exception as e:
                logging.error(f"Forwarding failed: {e}")
                
        try:
            payload = {"sender": sender, "recipient": recipients, "subject": original_subject, "body": body, "message_id": msg_id}
            # requests is imported at top level
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            logging.error(f"Webhook failed: {e}")
            
    except Exception as e:
        logging.error(f"Critical Script Error: {e}")
    sys.exit(0)

if __name__ == "__main__":
    main()
