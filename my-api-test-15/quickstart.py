from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/keep/']

# The ID of a sample document.
DOCUMENT_IDS_LIST = ['1Yhuc17bWVrJY8bUBLKKEzCXFzWzY1M0nzIm1GdyYsZ0']


def get_creds():
    """
    get creds for user.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_doc(creds, doc_ids_list):
    for doc_id in doc_ids_list:
        try:
            service_docs = build('docs', 'v1', credentials=creds)
            service_keep = build('keep', 'v1', credentials=creds)
            # Retrieve the documents contents from the Docs service.
            document = service_docs.documents().get(documentId=doc_id).execute()
            keep_note = service_keep
            print('The title of the document is: {}'.format(document.get('title')))
        except HttpError as err:
            print(err)


if __name__ == '__main__':
    creds = get_creds()
    get_doc(creds, DOCUMENT_IDS_LIST)
