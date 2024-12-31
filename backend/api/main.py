from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
import os
import time
from api.Authenticate_user import authenticate_user, load_service  # Import functions from authenticate.py
from api.Delete_emails import delete_emails_based_on_params
from api.Email_notifier import monitor_emails
from pydantic import BaseModel
import tempfile

# Initialize FastAPI application
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://mail-ease-qoty-8y58zjvxo-aabid2947s-projects.vercel.app"],  # Update with allowed domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

# Pydantic models for request bodies
class Criteria(BaseModel):
    criteria: dict

class Preference(BaseModel):
    preference: dict

@app.post("/authenticate")
async def authenticate_user_endpoint(file: UploadFile = File(...)):
    # Save the uploaded credentials file to the local system
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())
    
    time.sleep(1)  # Wait for file to be written
    
    try:
        # Call the authenticate_user function from authenticate.py
        uuid = authenticate_user(file_path)
        return {"message": f"Your uuid for further requests is: {uuid}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")
    finally:
        os.remove(file_path)  # Cleanup by removing the uploaded file

@app.post("/delete-emails")
async def delete_emails(criteria: Criteria):
    print(criteria.criteria.get("uuid"))
    service = load_service(criteria.criteria.get("uuid"))
    if not service:
        raise HTTPException(status_code=400, detail="Authentication required")
    await delete_emails_based_on_params(service=service, criteria=criteria.criteria)
    return {"message": "Email deletion completed!"}

@app.post("/monitor-mails")
async def notify_user(preference: Preference, background_tasks: BackgroundTasks):
    service = load_service(preference.preference.get("uuid"))
    if not service:
        raise HTTPException(status_code=400, detail="Authentication required")

    # Run monitor_emails as a background task
    background_tasks.add_task(monitor_emails, service=service, preferences=preference.preference)
    
    return {"message": "Email monitoring started!"}

# Health check endpoint to verify if the API is running
@app.get("/")
async def health_check():
    return {"status": "running", "message": "Email Cleaner API is active."}
