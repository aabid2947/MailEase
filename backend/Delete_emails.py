import time
import re

# Function to check if an email is useful based on the user-selected criteria
def is_email_useful(service,message, criteria,senders_count):
        # Fetch full email details to include 'internalDate' and other message details
        email_details = service.users().messages().get(userId='me', id=message['id']).execute()
            
         # Extract sender email
        sender_email = None
        headers = email_details.get('payload', {}).get('headers', [])
        for header in headers:
            if header.get('name') == 'From':
                match = re.search(r'<(.+)>', header.get('value'))
                if match:
                    sender_email = match.group(1)

                    sender = match.group(1)  # Extract the email inside the angle brackets
                
        if sender_email:
            # Update the senders count
            senders_count[sender_email] = senders_count.get(sender_email, 0) + 1

            # Check if the sender exceeds the message threshold
            if senders_count[sender_email] > 5:
                print(f"Exceeded threshold: {sender_email} ({senders_count[sender_email]} messages)")
                return False  # Mark email for deletion
        else:
            print(f"Warning: No sender email found for message ID {message['id']}")
            return False

            # Apply the criteria based on the dictionary values

            # Check for age criteria
        if criteria.get('age', True):  # Default to True if not specified
                # Ensure internalDate exists
                if 'internalDate' not in email_details:
                    print(f"Error: internalDate not found for message ID {message['id']}")
                    return False  # Skip this email if it doesn't have internalDate

                # Get the email's timestamp (in milliseconds)
                email_timestamp = int(email_details['internalDate']) / 1000  # Convert to seconds
                current_timestamp = time.time()  # Current time in seconds
                six_months_in_seconds = 6 * 30 * 24 * 60 * 60  # 6 months in seconds
                
                if current_timestamp - email_timestamp > six_months_in_seconds:
                    print(current_timestamp - email_timestamp)
                    return False  # Email is older than 6 months, considered not useful

        # Check if the email is in the spam folder (if applicable)
        if criteria.get('spam', True):  # Default to True if not specified
                if 'SPAM' in email_details.get('labelIds', []):
                    return False

        # Check for sender (e.g., known senders or suspicious domain)
        if criteria.get('sender', True):  # Default to True if not specified
                sender = email_details.get('payload', {}).get('headers', [])
                sender_email = None
                for header in sender:
                    if header.get('name') == 'From':
                        sender_email = header.get('value')
                if sender_email and (sender_email.endswith('@spamdomain.com') or sender_email.startswith('no-reply')):
                    return False

        # Check if the sender is in the specified list of senders to delete
        if criteria.get('specific_senders', False):  # Check if specific senders list exists
                specific_senders = criteria.get('specific_senders', [])
                sender_email = email_details.get('payload', {}).get('headers', [])
                
                sender = None
                for header in sender_email:
                    if header.get('name') == 'From':
                    
                    # Extract the email address using a regex
                        match = re.search(r'<(.+)>', header.get('value'))
                        if match:
                            sender = match.group(1)  # Extract the email inside the angle brackets
                
                if sender and sender in specific_senders:
                    print(sender)
                    return False  # If the sender is in the list, mark for deletion

        # Check for subject keywords (e.g., promotional or generic subjects)
        if criteria.get('subject', True):  # Default to True if not specified
                
                # Keywords for the subject
                subject_keywords = ['free', 'offer', 'unsubscribe', 'special', 'reset password', 'otp', 'account verification', 'verify your account', 'security code', 'authentication code', 'activation link']
                
                subject = email_details.get('payload', {}).get('headers', [])
                subject_text = None
                for header in subject:
                    if header.get('name') == 'Subject':
                        subject_text = header.get('value')
                if subject_text and any(keyword in subject_text.lower() for keyword in subject_keywords):
                    return False

        # Check if the email body is mostly promotional content
        if criteria.get('body', True):  # Default to True if not specified
                # Keywords for the email body
                body_keywords = ['limited time', 'buy now', 'exclusive offer', 'reset password', 'otp', 'account verification', 'confirm email', 'activation link', 'sign up confirmation', 'verify your account']

                body = email_details.get('snippet', '')
                if body and any(keyword in body.lower() for keyword in body_keywords):
                    return False

         # Check for attachments larger than a certain size (e.g., 10MB)
        if criteria.get('attachments', True):  # Default to True if not specified
                parts = email_details.get('payload', {}).get('parts', [])
                for part in parts:
                    if part.get('body', {}).get('size', 0) > 10 * 1024 * 1024:  # 10MB
                        return False

        # Check for unread or inactive emails (if applicable)
        if criteria.get('unread', True):  # Default to True if not specified
                if 'UNREAD' not in email_details.get('labelIds', []):
                    return False

        return True

async  def delete_emails_based_on_params(service, criteria):
    page_token = None
    senders_count = {}

    while True:
        # Fetch the list of email messages (this provides only basic information)
        results = service.users().messages().list(userId='me',pageToken=page_token).execute()
        messages = results.get('messages', [])
        

        print(len(messages))
        # Loop through emails and delete those that aren't useful based on the criteria
        for message in messages:
            if not  is_email_useful(service,message, criteria,senders_count):
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
    'spam': False,       # Check if the email is in the spam folder
    'sender': False,    # Don't check the sender (unless specified in specific_senders)
    'subject': True,    # Check the subject for promotional keywords
    'body': True,      # Don't check the body content
    'attachments': False, # Check if attachments are larger than 10MB
    'unread': False,     # Check if the email is unread or inactive
    'specific_senders': [],  # List of senders to delete all emails from
    'message_threshold':5
}

