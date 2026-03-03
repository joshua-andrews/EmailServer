import asyncio
import logging
import email
from email import policy
from aiosmtpd.controller import Controller
import requests
import sys

# Configuration
WEBHOOK_URL = "https://web-production-48500.up.railway.app/webhook"
LOG_FILE = "/var/log/email-webhook.log"
HOST = "127.0.0.1"
PORT = 10025

# Setup Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s %(message)s')

class WebhookHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            content = envelope.content.decode('utf8', errors='replace')
            msg = email.message_from_string(content, policy=policy.default)
            
            sender = envelope.mail_from
            recipient = envelope.rcpt_tos[0]
            subject = msg['subject'] or "(No Subject)"
            
            # Simple Body Extraction
            body = " (No Body) "
            try:
                # Prefer plain text, fallback to html
                body_part = msg.get_body(preferencelist=('plain', 'html'))
                if body_part:
                    body = body_part.get_content()
            except Exception as e:
                logging.error(f"Body parsing error: {e}")

            # Send to Webhook
            payload = {
                "sender": sender,
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "message_id": msg.get('Message-ID', 'unknown')
            }
            
            logging.info(f"Forwarding email from {sender} to {recipient}")
            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                logging.info(f"Webhook response: {response.status_code} - {response.text}")
            except Exception as req_err:
                logging.error(f"Webhook request failed: {req_err}")
            
            return '250 OK'
        except Exception as e:
            logging.error(f"Critical error processing email: {e}")
            return '451 Processing Error'

if __name__ == "__main__":
    print(f"Starting Email Webhook Bridge on {HOST}:{PORT}...")
    logging.info("Starting Service")
    controller = Controller(WebhookHandler(), hostname=HOST, port=PORT)
    controller.start()
    
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
