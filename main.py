import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.https import MediafileUpload
import os


class MyDrive:
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API."""

        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def list_files(self,page_size="10"):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))


    def upload_files(self,filename,path):
        folder_id="1XLeFvsgBbnagvMM20ptRH3PAnNK6QDDE"
        media=MediafileUpload(f"{path}{filename}")

        response=self.service.files().list(
            q=f"name='{filename}' and parents='{folder_id}'",
            space="drive",
            fields="nextPageToken,files(id,name)",
            pageToken=None).execute()

        if len(response["files"])==0:
            files_metadata={
                "name":filename,
                "parents":[folder_id]
            }
            file=self.service.files().create(body=files_metadata,media_body=media,fields="id").execute()
            print(f"A new file was created {file.get('id')}")

        else:
            for file in response.get('files',[]):
                #process change
                update_file=self.service.files().update(
                    fileId=file.get('id'),
                    media_body=media)
                ).execute()
                print(update_file)
                print(f"Updated file")


def main():
    path="/home/jarvis/competitive"
    files=os.listdir(path)
    my_drive=MyDrive()
    #my_drive.list_files()


    for items in files:
        my_drive.upload_files(item,path)




if __name__ == '__main__':
    main()
