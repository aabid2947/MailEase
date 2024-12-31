import firebase_admin
from firebase_admin import credentials, firestore
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from fastapi import HTTPException
import pickle
import uuid
import os
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# Constants
SCOPES = ['https://mail.google.com/']  # Gmail API scope

# Retrieve the Firebase credentials (encoded in base64) from environment variables
encoded_credential = os.getenv('FIREBASE_CREDENTIALS')

if encoded_credential:
    # Decode the base64 credentials and initialize Firebase Admin SDK
    decoded_credentials = base64.b64decode(encoded_credential).decode('utf-8')
    cred = credentials.Certificate(eval(decoded_credentials))
    try:
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully!")
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
else:
    print("Firebase credentials are not set.")

# Firestore client
db = firestore.client()

# Function to save the Gmail service to Firebase Firestore
def save_service_to_firestore(service, user_id):
    try:
        service_data = pickle.dumps(service)
        doc_ref = db.collection('gmail_services').document(user_id)
        doc_ref.set({'service': service_data})
        print(f"Service for user {user_id} saved successfully.")
    except Exception as e:
        print(f"Error saving service to Firestore: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload service to Firestore: {str(e)}")

# Function to load the Gmail API service from Firebase Firestore
def load_service(user_id):
    try:
        doc_ref = db.collection('gmail_services').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            service_data = doc.to_dict().get('service')
            service = pickle.loads(service_data)
            return service
        else:
            print(f"No service found for user {user_id}.")
            return None
    except Exception as e:
        print(f"Error loading service for user {user_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Failed to load service from Firestore: {str(e)}")

# Function to authenticate the user and save the credentials
def authenticate_user(credentials_path: str):
    try:
        # Configure redirect URI dynamically if required for deployment (e.g., Vercel)
        redirect_uri = os.getenv('OAUTH_REDIRECT_URI', 'https://your-production-url.com/callback')  # Update this with your actual redirect URL
        
        # Set up OAuth flow and authenticate
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        # flow.redirect_uri = redirect_uri
        creds = flow.run_local_server(port=4000)

        # creds = flow.run_local_server(port=0)  # Uses a random available port, adjust if needed
        service = build('gmail', 'v1', credentials=creds)
        
        unique_id = str(uuid.uuid4())  # Unique ID for the user
        save_service_to_firestore(service, unique_id)
        
        return unique_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

