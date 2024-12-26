from twilio.rest import Client

import re
from datetime import datetime, timedelta
import base64
import time
from Authenticate_email import authenticate_user

# Twilio credentials
# add your own credentials here
client = Client(account_sid, auth_token)

# Notification preferences
USER_PREFERENCES = {
    "email_addresses": ["aabidhussainpas@gmail.com"],  # Emails to monitor
    "keywords": ["important", "scheduled meeting", "test OTP", "reset password", "urgent"],
    "user_phone_number": "+918264782290",  # User's phone number for notifications
}

def fetch_emails(service, last_check_time):
    """
    Fetch emails from Gmail received after `last_check_time`.
    """
    query = f"after:{int(last_check_time.timestamp())}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_details(service, message_id):
    """
    Get details of an email using its message ID.
    """
    message = service.users().messages().get(userId='me', id=message_id).execute()
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    body = payload.get('body', {}).get('data', '')

    # Get email subject and sender
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)
    sender = next((h['value'] for h in headers if h['name'] == 'From'), None)

    # Decode body if necessary
    if body:
        body = base64.urlsafe_b64decode(body).decode('utf-8', errors='ignore')

    return {
        "subject": subject,
        "sender": sender,
        "body": body
    }

def match_criteria(email_details, preferences):
    """
    Check if the email matches user-defined criteria.
    """
    keywords = preferences['keywords']
    monitored_emails = preferences['email_addresses']

    # Check if sender is in monitored emails
    if any(email in email_details['sender'] for email in monitored_emails):
        return "specified target email"

    # Check for keywords in subject or body
    for keyword in keywords:
        if re.search(rf'\b{keyword}\b', email_details['subject'], re.IGNORECASE) or \
           re.search(rf'\b{keyword}\b', email_details['body'], re.IGNORECASE):
            return f"important due to the keyword '{keyword}'"

    return None

def send_message(message,user_whatsapp_number):

    # Send message
    client.messages.create(
    from_='whatsapp:+14155238886',  # Twilio WhatsApp sandbox number
    body=message,  # Use 'body' for custom messages
    to=f'whatsapp:{user_whatsapp_number}'  # Recipient's WhatsApp number
    )

    print(message)

def send_notification(preferences, email_details, context):
    """
    Send an email notification about the matched email.
    """
    notification_message = (
        f"New email from {email_details['sender']}:\n"
        f"Subject: {email_details['subject']}\n"
        f"This email is {context}.\n"
        "Please check it promptly for important information."
    )
    send_message(notification_message,preferences['user_phone_number'])

def monitor_emails(service, preferences):
    """
    Continuously monitor emails and provide real-time updates.
    Args:
        service: Gmail API service object.
        preferences: User preferences for monitoring.
        interval: Time interval (in seconds) to check for new emails.
    """
    # Set initial check time to the current time
    last_check_time = datetime.utcnow()
    processed_message_ids = set()  # To track already processed message IDs

    while True:
        print("Checking for new emails...")
        emails = fetch_emails(service, last_check_time)
        new_check_time = datetime.utcnow()  # Update check time for the next cycle

        for email in emails:
            # Process only new emails received since the last check
            if email['id'] not in processed_message_ids:
                email_details = get_email_details(service, email['id'])
                context = match_criteria(email_details, preferences)
                if context:
                    send_notification(preferences, email_details, context)
                processed_message_ids.add(email['id'])  # Mark email as processed

        # Update the last check time to avoid processing old emails
        last_check_time = new_check_time

        # Wait before checking again
        time.sleep(preferences['interval'])
        
if __name__ == "__main__":
    service = authenticate_user()
    # Continuously monitor emails
    monitor_emails(service, USER_PREFERENCES)  # Check every 5 minutes
