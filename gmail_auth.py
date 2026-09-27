import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# only readonly access allowed, we are not sending/deleting anything
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE): # if logged-in before, load the token from file
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # if there is no token or the current token is invalid
    if not creds or not creds.valid:
        # if token expired, refresh it.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        # if first time login,open browser so the user can log in and approve
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # save the new/refreshed token to file for next time
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            
    # build and return the authorized gmail client ready to use
    return build("gmail", "v1", credentials=creds)