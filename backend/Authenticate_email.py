from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://mail.google.com/']

def authenticate_user():
    flow = InstalledAppFlow.from_client_secrets_file(r'C://Users//aabid//OneDrive//Desktop//EmailCleaner//backend//credentials//credentials.json', SCOPES)
    creds = flow.run_local_server(port=4000)
    service = build('gmail', 'v1', credentials=creds)
    return service






