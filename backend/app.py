from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
from Delete_emails import delete_emails_based_on_params
from fastapi.middleware.cors import CORSMiddleware
from Email_notifier import monitor_emails
import time


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

SCOPES = ['https://mail.google.com/']
UPLOAD_FOLDER = 'credentials'
SERVICE_FOLDER = 'services'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SERVICE_FOLDER, exist_ok=True)

# Pydantic model for request body
class Criteria(BaseModel):
    criteria: dict
    
class Preference(BaseModel):
    preference: dict

def save_service(service, user_id):
    service_file = os.path.join(SERVICE_FOLDER, f"{user_id}_service.pkl")
    with open(service_file, 'wb') as f:
        pickle.dump(service, f)

def load_service(user_id):
    service_file = os.path.join(SERVICE_FOLDER, f"{user_id}_service.pkl")
    if os.path.exists(service_file):
        with open(service_file, 'rb') as f:
            return pickle.load(f)
    return None

@app.post("/authenticate")
async def authenticate_user(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())
        
    time.sleep(1)
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(file_path, SCOPES)
        creds = flow.run_local_server(port=4000)
        service = build('gmail', 'v1', credentials=creds)
        save_service(service, "default_user")
        return {"message": "Authentication successful!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")
    finally:
        os.remove(file_path)

@app.post("/delete-emails")
async def delete_emails(criteria: Criteria):
    service = load_service("default_user")
    if not service:
        raise HTTPException(status_code=400, detail="Authentication required")
    await delete_emails_based_on_params(service=service, criteria=criteria.criteria)
    return {"message": "Email deletion completed!"}

@app.post("/monitor-mails")
async def notify_user(preference:Preference):
     
    service = load_service("default_user")
    if not service:
        raise HTTPException(status_code=400, detail="Authentication required")
    await monitor_emails(service=service, preferences=preference.preference)
    return {"message": "Email monitoring started!"}


@app.get("/health-check")
async def health_check():
    return {"status": "running", "message": "Email Cleaner API is active."}

# Run the FastAPI application with Uvicorn
# uvicorn app:app --reload
