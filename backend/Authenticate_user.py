import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from fastapi import HTTPException
import time

# Define the folder to store the credentials and service files
UPLOAD_FOLDER = 'credentials'  # Folder to store uploaded credentials
SERVICE_FOLDER = 'services'    # Folder to store the saved Gmail API service file

# Create the folders if they don't already exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SERVICE_FOLDER, exist_ok=True)

# Define the Google API scopes required for accessing Gmail
SCOPES = ['https://mail.google.com/']  # Scope for Gmail access

def save_service(service, user_id):
    """
    Save the Gmail service to a file for future use.
    
    Args:
        service: The Gmail API service object to be saved.
        user_id: The unique identifier for the user (used to name the service file).
    """
    # Define the path where the service file will be stored
    service_file = os.path.join(SERVICE_FOLDER, f"{user_id}_service.pkl")
    
    # Open the file and save the service object using pickle
    with open(service_file, 'wb') as f:
        pickle.dump(service, f)

def load_service(user_id):
    """
    Load the Gmail service from a previously saved file.
    
    Args:
        user_id: The unique identifier for the user (used to load the service file).
        
    Returns:
        The saved Gmail API service object, or None if not found.
    """
    # Define the path to the service file
    service_file = os.path.join(SERVICE_FOLDER, f"{user_id}_service.pkl")
    
    # Check if the service file exists
    if os.path.exists(service_file):
        # Load the service object from the file using pickle
        with open(service_file, 'rb') as f:
            return pickle.load(f)
    
    # Return None if the service file does not exist
    return None

def authenticate_user(file_path: str):
    """
    Authenticate the user using the OAuth flow and return the Gmail service object.
    
    Args:
        file_path: The path to the credentials file used for authentication.
        
    Returns:
        service: The authenticated Gmail API service object.
        
    Raises:
        HTTPException: If the authentication process fails, an exception is raised.
    """
    try:
        # Start the OAuth flow to authenticate the user
        flow = InstalledAppFlow.from_client_secrets_file(file_path, SCOPES)
        
        # Run the local server to complete the authentication
        creds = flow.run_local_server(port=4000)
        
        # Build the Gmail API service using the obtained credentials
        service = build('gmail', 'v1', credentials=creds)
        
        # Save the authenticated service for future use
        save_service(service, "default_user")
        
        # Return the authenticated service
        return service
    except Exception as e:
        # Raise an exception if authentication fails
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")
