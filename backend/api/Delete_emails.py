import time
import re

# Function to extract sender email from the email headers
def extract_sender_email(email_details):
    headers = email_details.get('payload', {}).get('headers', [])
    for header in headers:
        if header.get('name') == 'From':
            match = re.search(r'<(.+)>', header.get('value'))
            if match:
                return match.group(1)  # Return the email inside the angle brackets
    return None

# Function to check if the email is older than 6 months
def check_age(email_details, current_timestamp):
    if 'internalDate' not in email_details:
        print(f"Error: internalDate not found")
        return False
    
    email_timestamp = int(email_details['internalDate']) / 1000  # Convert to seconds
    six_months_in_seconds = 6 * 30 * 24 * 60 * 60  # 6 months in seconds
    if current_timestamp - email_timestamp > six_months_in_seconds:
        print(f"Email is older than 6 months")
        return False
    return True

# Function to check if the email is marked as spam
def check_spam(email_details):
    if 'SPAM' in email_details.get('labelIds', []):
        print("Email is in spam folder")
        return False
    return True

# Function to check if the sender is suspicious or blacklisted
def check_sender(sender_email, criteria):
    if sender_email:
        # Check if the sender matches the suspicious criteria
        if sender_email.endswith('@spamdomain.com') or sender_email.startswith('no-reply'):
            print(f"Sender {sender_email} is suspicious")
            return False
    return True

# Function to check if the sender is in the specific list of senders to delete
def check_specific_senders(sender_email, criteria):
    specific_senders = criteria.get('specific_senders', [])
    if sender_email in specific_senders:
        print(f"Sender {sender_email} is in the specific senders list")
        return False
    return True

# Function to check the subject for promotional keywords
def check_subject(email_details):
    subject_keywords = ['free', 'offer', 'unsubscribe', 'special', 'reset password', 'otp', 'account verification', 'verify your account', 'security code', 'authentication code', 'activation link']
    headers = email_details.get('payload', {}).get('headers', [])
    for header in headers:
        if header.get('name') == 'Subject':
            subject_text = header.get('value')
            if any(keyword in subject_text.lower() for keyword in subject_keywords):
                print("Subject contains promotional keywords")
                return False
    return True

# Function to check the email body for promotional content
def check_body(email_details):
    body_keywords = ['limited time', 'buy now', 'exclusive offer', 'reset password', 'otp', 'account verification', 'confirm email', 'activation link', 'sign up confirmation', 'verify your account']
    body = email_details.get('snippet', '')
    if any(keyword in body.lower() for keyword in body_keywords):
        print("Body contains promotional content")
        return False
    return True

# Function to check if the email has large attachments
def check_attachments(email_details):
    parts = email_details.get('payload', {}).get('parts', [])
    for part in parts:
        if part.get('body', {}).get('size', 0) > 10 * 1024 * 1024:  # 10MB
            print("Email has attachments larger than 10MB")
            return False
    return True

# Function to check if the email is unread
def check_unread(email_details):
    if 'UNREAD' not in email_details.get('labelIds', []):
        print("Email is not unread")
        return False
    return True

# Main function to check if an email is useful based on the provided criteria
def is_email_useful(service, message, criteria, senders_count):
    # Fetch full email details to include 'internalDate' and other message details
    email_details = service.users().messages().get(userId='me', id=message['id']).execute()

    # Extract sender email and check if it's valid
    sender_email = extract_sender_email(email_details)
    if not sender_email:
        print(f"Warning: No sender email found for message ID {message['id']}")
        return False

    # Update the sender count
    senders_count[sender_email] = senders_count.get(sender_email, 0) + 1

    # Check if the sender exceeds the threshold
    if senders_count[sender_email] > criteria.get('message_threshold', 5):
        print(f"Exceeded message threshold: {sender_email}")
        return False  # Mark email for deletion

    # Apply the criteria based on the dictionary values
    current_timestamp = time.time()

    # Check if the email is older than 6 months
    if criteria.get('age', True) and not check_age(email_details, current_timestamp):
        return False

    # Check if the email is in the spam folder
    if criteria.get('spam', True) and not check_spam(email_details):
        return False

    # Check if the sender is suspicious
    if criteria.get('sender', True) and not check_sender(sender_email, criteria):
        return False

    # Check if the sender is in the specific senders list
    if criteria.get('specific_senders', False) and not check_specific_senders(sender_email, criteria):
        return False

    # Check for subject keywords
    if criteria.get('subject', True) and not check_subject(email_details):
        return False

    # Check if the body contains promotional content
    if criteria.get('body', True) and not check_body(email_details):
        return False

    # Check for attachments larger than 10MB
    if criteria.get('attachments', True) and not check_attachments(email_details):
        return False

    # Check if the email is unread
    if criteria.get('unread', True) and not check_unread(email_details):
        return False

    return True


async def delete_emails_based_on_params(service, criteria):
    page_token = None
    senders_count = {}

    while True:
        # Fetch the list of email messages (this provides only basic information)
        results = service.users().messages().list(userId='me', pageToken=page_token).execute()
        messages = results.get('messages', [])

        print(len(messages))
        # Loop through emails and delete those that aren't useful based on the criteria
        for message in messages:
            if not is_email_useful(service, message, criteria, senders_count):
                try:
                    service.users().messages().delete(userId='me', id=message['id']).execute()
                    print(f"Deleted email with ID: {message['id']}")
                except Exception as e:
                    print(f"Error deleting email with ID {message['id']}: {e}")

        # Check if there is a next page token, if not, stop the loop
        page_token = results.get('nextPageToken')
        print(senders_count)

        if not page_token:
            break


# Example of how to call the function with the criteria
criteria = {
    'age': True,        # Check if the email is older than 6 months
    'spam': False,      # Check if the email is in the spam folder
    'sender': False,    # Don't check the sender (unless specified in specific_senders)
    'subject': True,    # Check the subject for promotional keywords
    'body': True,       # Don't check the body content
    'attachments': False, # Check if attachments are larger than 10MB
    'unread': False,    # Check if the email is unread or inactive
    'specific_senders': [],  # List of senders to delete all emails from
    'message_threshold': 5
}
