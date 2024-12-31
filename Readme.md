# MailEase

# Purpose
MailEase is a SaaS solution designed to help users manage their emails efficiently. It offers two main features:

# 1. Email Monitoring and Notifications
- Monitors user emails and sends notifications via WhatsApp when important emails arrive.
- Users can customize criteria for identifying important emails by specifying:
  - Targeted email addresses.
  - Keywords to search in the email subject or body.
  - A phone number to receive notifications.

Example user preferences configuration:

USER_PREFERENCES = {
    "email_addresses": ["aabidhussainpas@gmail.com"],
    "keywords": ["important", "scheduled meeting", "test OTP", "reset password", "urgent"],
    "user_phone_number": "+918264782290",
}


# 2. Email Deletion
Helps users delete unused, old, spam, or emails from specific senders based on customizable criteria.

Example deletion criteria:

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


# Firebase Integration for Service Storage
- User configurations are saved securely in Firebase.
- Each user's service configuration is identified using a unique UUID, allowing for easy management and tracking.

# Features
- Customizable Monitoring: Configure criteria to identify important emails.
- Targeted Email Deletion: Remove emails based on various criteria like sender, age, and subject.
- WhatsApp Notifications: Receive immediate notifications on WhatsApp for important emails.
- Firebase Storage: User data is securely stored with Firebase, identified by unique UUIDs.

---

# Installation Instructions

# Frontend Setup
1. Navigate to the frontend folder.
2. Install the required npm packages:
   npm install

3. Start the development server:
   npm run dev

# Backend Setup (Firebase & Twilio)

# Install Dependencies:
   pip install -r requirements.txt

# Firebase Setup:
1. Create a Firebase project by following the instructions on the [Firebase Console](https://console.firebase.google.com/).
2. Set up Firestore to store user configurations.
3. Download the Firebase credentials (`firebase-adminsdk.json`) from the Firebase console.
4. Place the `firebase-adminsdk.json` file in your backend directory and generate a base64 equivalent and save it in `.env`.

# Twilio Setup:
1. Sign up for Twilio and create a WhatsApp-enabled number.

2. Add your Twilio credentials (Account SID, Auth Token, WhatsApp number) in `.env` for sending WhatsApp notifications.

#### Run the Backend Server:
1. Start the FastAPI backend server:
   uvicorn app:app --reload

---

## Google API Setup

### Step 1: Enable Google API
1. Log in to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Gmail API for your project.
3. Create an OAuth 2.0 consent screen with the following scope:
4. 
   SCOPES = ['https://mail.google.com/']

5. Generate OAuth 2.0 credentials and download the `credentials.json` file.

# Step 2: Upload Credentials and Authenticate
1. Visit the website and navigate to the "Navigation" section.
2. Upload the `credentials.json` file.
3. Click "Authenticate." You will be redirected to Gmail for confirmation.
4. Grant the necessary permissions to enable the features.

# Step 3: Use the Features
1. Navigate to the Email Notifier or Delete Emails section.
2. Select your criteria and activate monitoring or deletion as needed.

---

## Technologies Used

### Backend:
- Python
- FastAPI
- Firebase (for service storage)
- Google API Client
- Google Auth OAuthlib
- Twilio API (for WhatsApp notifications)

### Frontend:
- Node.js
- Vite
- React
- Framer

### Third-party Services:
- Twilio for WhatsApp notifications
- Firebase for service data storage
