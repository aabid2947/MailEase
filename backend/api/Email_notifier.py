from twilio.rest import Client
import re
from datetime import datetime
import base64
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

# Twilio credentials (Replace with actual credentials)

client = Client(account_sid, auth_token)

# Notification preferences - Customizable settings for monitoring
USER_PREFERENCES = {
    "email_addresses": ["aabidhussainpas@gmail.com"],  # List of emails to monitor
    "keywords": ["important", "scheduled meeting", "test OTP", "reset password", "urgent"],  # Keywords to look for
    "user_phone_number": "+918264782290",  # User's phone number for notifications
    "interval": 60  # Interval in seconds to check for new emails (default: 1 minute)
}

def fetch_emails(service, last_check_time):
    """
    Fetch emails from Gmail that were received after `last_check_time`.
    
    Args:
        service: Gmail API service object.
        last_check_time: The datetime object marking the last check time.
        
    Returns:
        List of emails received after the given time.
    """
    query = f"after:{int(last_check_time.timestamp())}"  # Query for emails after the given timestamp
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_details(service, message_id):
    """
    Retrieve the details of a specific email using its message ID.
    
    
    Args:
        service: Gmail API service object.
        message_id: The unique ID of the email message.
        
    Returns:
        Dictionary with the subject, sender, and body of the email.
    """
    message = service.users().messages().get(userId='me', id=message_id).execute()
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    body = payload.get('body', {}).get('data', '')

    # Extract subject and sender from email headers
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)
    sender = next((h['value'] for h in headers if h['name'] == 'From'), None)

    # Decode email body if it's encoded
    if body:
        body = base64.urlsafe_b64decode(body).decode('utf-8', errors='ignore')

    return {
        "subject": subject,
        "sender": sender,
        "body": body
    }

def match_criteria(email_details, preferences):
    """
    Check if the email matches the user's defined criteria (e.g., keywords, sender).
    
    Args:
        email_details: Dictionary with the subject, sender, and body of the email.
        preferences: User's notification preferences.
        
    Returns:
        A string describing why the email matches the criteria, or None if it doesn't.
    """
    keywords = preferences['keywords']
    monitored_emails = preferences['email_addresses']

    # Check if the sender is one of the monitored emails
    if any(email in email_details['sender'] for email in monitored_emails):
        return "specified target email"

    # Check for any matching keywords in subject or body
    for keyword in keywords:
        if re.search(rf'\b{keyword}\b', email_details['subject'], re.IGNORECASE) or \
           re.search(rf'\b{keyword}\b', email_details['body'], re.IGNORECASE):
            return f"important due to the keyword '{keyword}'"

    return None  # No match found

def send_message(message, user_whatsapp_number):
    """
    Send a WhatsApp message using Twilio's API.
    
    Args:
        message: The message content to be sent.
        user_whatsapp_number: The recipient's WhatsApp number.
    """
    # Send message via Twilio's WhatsApp API
    client.messages.create(
        from_='whatsapp:+14155238886',  # Twilio WhatsApp sandbox number
        body=message,  # Message body content
        to=f'whatsapp:{user_whatsapp_number}'  # Recipient's WhatsApp number
    )

    print(message)  # Print message for confirmation

def send_notification(preferences, email_details, context):
    """
    Send an email notification about the matched email.
    
    Args:
        preferences: User's preferences (email addresses, phone number).
        email_details: The details of the matched email.
        context: The reason why the email was flagged (e.g., keyword match).
    """
    # Construct the notification message
    notification_message = (
        f"New email from {email_details['sender']}:\n"
        f"Subject: {email_details['subject']}\n"
        f"This email is {context}.\n"
        "Please check it promptly for important information."
    )
    
    # Send the notification message via WhatsApp
    send_message(notification_message, preferences['user_phone_number'])

def monitor_emails(service, preferences):
    """
    Continuously monitor emails and provide real-time updates.
    
    Args:
        service: Gmail API service object.
        preferences: User preferences for monitoring.
    """
    # Initialize the last check time to the current time
    last_check_time = datetime.now(timezone.utc)
    processed_message_ids = set()  # Set to keep track of processed email IDs

    while True:
        print("Checking for new emails...")
        
        # Fetch emails received after the last check time
        emails = fetch_emails(service, last_check_time)
        
        # Update the last check time for the next cycle
        new_check_time = datetime.now(timezone.utc)

        # Process each new email
        for email in emails:
            # Only process emails that haven't been processed yet
            if email['id'] not in processed_message_ids:
                email_details = get_email_details(service, email['id'])
                context = match_criteria(email_details, preferences)  # Check if email matches criteria
                
                if context:  # If the email matches the criteria, send a notification
                    send_notification(preferences, email_details, context)
                
                # Mark the email as processed
                processed_message_ids.add(email['id'])

        # Update the last check time to avoid processing old emails again
        last_check_time = new_check_time

        # Wait before checking for new emails again
       
        time.sleep(int(preferences['interval'])*60)

# Example of calling the monitor_emails function
# Assuming 'service' is already authenticated Gmail API service object
# monitor_emails(service, USER_PREFERENCES)
