import os.path
import base64

from django.http     import JsonResponse

from google.auth.transport.requests import Request
from google.oauth2.credentials      import Credentials
from google_auth_oauthlib.flow      import InstalledAppFlow
from googleapiclient.discovery      import build
from  email.message                 import EmailMessage
import google.auth

SCOPES =['https://www.googleapis.com/auth/gmail.send']

class GoogleEmail:
    def __init__(self, credentials):
        self.credentials = credentials

    def generate_token(self, file_path):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
    
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def send_email(self, content, author, sender_email, creds):
        
        service = build('gmail', 'v1', credentials=creds)

        content = "제안자 : " + sender_email + "/n" + "제안 내용 : " + content

        message = EmailMessage()

        message.set_content(content)

        message['To']      = author.user.email
        message['From']    = "ebsgreat7@gmail.com"
        message['Subject'] = "작가" + author.user.name + '에게 제안메일 드립니다'

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message  = {
            'raw': encoded_message
        }

        send_message = service.users().messages().send(userId='me', body=create_message).execute()
        
        return JsonResponse({"message" : "SUCCESS"}, status=200)


