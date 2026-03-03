import boto3
import os
from dotenv import load_dotenv

# Load credentials from the email_api directory
dotenv_path = os.path.join(os.path.dirname(__file__), 'email_api', '.env')
load_dotenv(dotenv_path)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"

def send_test_email(from_email, to_email):
    ses = boto3.client(
        'ses',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    try:
        response = ses.send_email(
            Source=from_email,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': '🚀 Production Access Test'},
                'Body': {
                    'Text': {'Data': f'Success! This email was sent from {from_email} in production mode.'},
                    'Html': {'Data': f'<h1>Success!</h1><p>This email was sent from <b>{from_email}</b> in production mode.</p>'}
                }
            }
        )
        print(f"✅ Email sent successfully! From: {from_email} To: {to_email}")
        print(f"Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    from_addr = input("Enter the 'From' email address (e.g. josh.andrews@getcopyculture.com): ")
    to_addr = input("Enter the 'To' email address: ")
    send_test_email(from_addr, to_addr)
