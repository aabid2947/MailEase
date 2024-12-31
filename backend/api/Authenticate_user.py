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
    # Decode the base64 credentials
    decoded_credentials = base64.b64decode(encoded_credential).decode('utf-8')
    # Initialize Firebase Admin SDK with the in-memory JSON
    cred = credentials.Certificate(eval(decoded_credentials))
    
    try:
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully!")
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
else:
    print("Firebase credentials are not set in environment variables.")

# Firestore reference
db = firestore.client()

# Function to save the Gmail service to Firebase Firestore
def save_service_to_firestore(service, user_id):
    """
    Saves the Gmail API service to Firestore (as serialized data).
    
    Args:
        service: The Gmail API service object.
        user_id: The unique user identifier.
    """
    try:
        # Serialize the service object using pickle
        service_data = pickle.dumps(service)

        # Add service data to Firestore
        doc_ref = db.collection('gmail_services').document(user_id)
        doc_ref.set({'service': service_data})
        print(f"Service for user {user_id} saved successfully to Firestore.")
    except Exception as e:
        print(f"Error saving service to Firestore: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload service to Firestore: {str(e)}")

# Function to load the Gmail API service from Firebase Firestore
def load_service(user_id):
    """
    Loads the Gmail API service for a user from Firestore.
    
    Args:
        user_id: The unique user identifier.
    
    Returns:
        The Gmail API service object.
    """
    try:
        doc_ref = db.collection('gmail_services').document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            # Deserialize the service object from Firestore
            service_data = doc.to_dict().get('service')
            service = pickle.loads(service_data)
            
            # Build and return the Gmail API service
            return service
        else:
            print(f"No service found for user {user_id}.")
            return None
    except Exception as e:
        print(f"Error loading service for user {user_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Failed to load service from Firestore: {str(e)}")

# Function to authenticate the user and save the credentials
def authenticate_user(credentials_path: str):
    """
    Authenticates the user via OAuth, saves credentials to Firestore, 
    and builds the Gmail service for the user.

    Args:
        credentials_path: Path to the Google client credentials JSON file.
    
    Returns:
        The unique user ID (UUID) for the authenticated user.
    """
    try:
        # Modify the redirect URI for the correct production environment
        redirect_uri = os.getenv('OAUTH_REDIRECT_URI', 'https://your-production-url.com/callback')

        # Authenticate and build the Gmail API service
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        
        # Set the redirect URI to ensure it matches your production environment
        flow.redirect_uri = redirect_uri
        
        creds = flow.run_local_server(port=0)  # Using port=0 to auto-choose a free port
        service = build('gmail', 'v1', credentials=creds)
        
        # Generate a unique user ID and save the service to Firestore
        unique_id = str(uuid.uuid4())
        save_service_to_firestore(service, unique_id)
        
        return unique_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

