from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import time
from Authenticate_user import authenticate_user, save_service, load_service  # Import the functions from authentication.py
from Delete_emails import delete_emails_based_on_params
from Email_notifier import monitor_emails

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, can be modified for specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request bodies
class Criteria(BaseModel):
    criteria: dict

class Preference(BaseModel):
    preference: dict

# API endpoint to authenticate the user
@app.post("/authenticate")
async def authenticate_user_endpoint(file: UploadFile = File(...)):
    # Save the uploaded credentials file to the local system
    file_path = os.path.join('credentials', file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    # Wait for the file to be fully written before starting authentication
    time.sleep(1)

    try:
        # Call the function from authentication.py to authenticate and return the service
        service = authenticate_user(file_path)
        return {"message": "Authentication successful!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")
    finally:
        os.remove(file_path)  # Clean up by removing the uploaded credentials file

# API endpoint to delete emails based on provided criteria
@app.post("/delete-emails")
async def delete_emails(criteria: Criteria):
    service = load_service("default_user")
    if not service:
        raise HTTPException(status_code=400, detail="Authentication required")
    await delete_emails_based_on_params(service=service, criteria=criteria.criteria)
    return {"message": "Email deletion completed!"}

# API endpoint to monitor emails based on provided preferences
@app.post("/monitor-mails")
async def notify_user(preference: Preference):
    service = load_service("default_user")
    if not service:
        raise HTTPException(status_code=400, detail="Authentication required")
    await monitor_emails(service=service, preferences=preference.preference)
    return {"message": "Email monitoring started!"}

# Health check endpoint to verify if the API is running
@app.get("/")
async def health_check():
    return {"status": "running", "message": "Email Cleaner API is active."}
