# MailEase

## Purpose
This SaaS solution is designed to assist users in managing their emails efficiently. It provides two key features:

1. **Email Monitoring and Notifications:**
   - Monitors user emails and sends notifications to WhatsApp when important emails arrive.
   - Users can customize criteria for identifying important emails by specifying:
     - Targeted email addresses.
     - Keywords to search in email subject or body.
     - A phone number to receive notifications.
   
   Example user preferences configuration:
   ```python
   USER_PREFERENCES = {
       "email_addresses": ["aabidhussainpas@gmail.com"],
       "keywords": ["important", "scheduled meeting", "test OTP", "reset password", "urgent"],
       "user_phone_number": "+918264782290",
   }
   ```

2. **Email Deletion:**
   - Helps users delete unused, old, spam, or emails from specific senders based on customizable criteria.
   - Example deletion criteria:
     ```python
     criteria = {
         'age': True,        # Delete emails older than 6 months
         'spam': False,      # Skip emails in the spam folder
         'sender': False,    # Skip checking the sender
         'subject': True,    # Delete based on promotional keywords in the subject
         'body': True,       # Analyze body content for deletion
         'attachments': False, # Skip emails with large attachments (>10MB)
         'unread': False,    # Skip unread or inactive emails
         'specific_senders': [], # Specify senders for targeted deletion
         'message_threshold': 5  # Maximum emails to retain before deletion
     }
     ```

## Features
- **Customizable Monitoring:** Update criteria for important emails.
- **Targeted Deletion:** Remove emails based on criteria like age, sender, and content.
- **WhatsApp Notifications:** Notify users instantly when an important email arrives.

## Installation Instructions

### Frontend Setup
1. Navigate to the `frontend` folder.
2. Install required npm packages:

   npm install
   
3. Start the development server:
   
   npm run dev
  

### Backend Setup
1. Navigate to the `backend` folder.
2. Install Python dependencies:
   
   pip install -r requirements.txt

3. In Email_notifier.py upload your credentils for twilio
   
4. Run the FastAPI backend server:
   bash
   uvicorn app:app --reload
   

## Usage Instructions

### Step 1: Enable Google API
1. Log in to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Gmail API for your project.
3. Create an OAuth 2.0 consent screen with the following scope:
   ```python
   SCOPES = ['https://mail.google.com/']
   ```
4. Generate OAuth 2.0 credentials and download the `credentials.json` file.

### Step 2: Upload Credentials and Authenticate
1. Visit the website and navigate to the "Navigation" section.
2. Upload the `credentials.json` file.
3. Click "Authenticate." You will be redirected to Gmail for confirmation.
4. Grant the necessary permissions to enable the features.

### Step 3: Use the Features
1. Navigate to the **Email Notifier** or **Delete Emails** section.
2. Select your criteria and activate monitoring or deletion as needed.

## Technologies Used
- **Backend:** Python, FastAPI, Google API Client, Google Auth OAuthlib
- **Frontend:** Node.js, Vite, React, Framer
- **Third-party Services:** Twilio for WhatsApp notifications

## Additional Information
- Ensure your Gmail account has IMAP enabled for the monitoring and deletion features to function.
- Use the following links for additional help:
  - [How to Enable Gmail API](https://developers.google.com/gmail/api/quickstart/python)
  - [OAuth 2.0 Overview](https://developers.google.com/identity/protocols/oauth2)
- Notifications are currently configured for WhatsApp using the Twilio API. Ensure your phone number is verified with Twilio.

For any questions or issues, feel free to reach out to the support team.

