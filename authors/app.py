import os.path
import json
import base64

from django.views    import View
from django.http     import JsonResponse

from users.utils                    import login_decorator
from google.auth.transport.requests import Request
from google.oauth2.credentials      import Credentials
from google_auth_oauthlib.flow      import InstalledAppFlow
from googleapiclient.discovery      import build
from googleapiclient.errors         import HttpError
from authors.models                 import Author, Proposal, ProposalObject
from  email.message                 import EmailMessage
import google.auth

SCOPES =['https://www.googleapis.com/auth/gmail.send']

class ProposalView(View):
    @login_decorator
    def post(self, request, author_id):
        try:
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

            data            = json.loads(request.body)
            content         = data["content"]
            sender_email    = data["sender_email"]
            proposal_object = data["proposal_object"]
            author          = Author.objects.get(id=author_id)

            Proposal.objects.create(
                sender_email       = sender_email,
                content            = content,
                proposal_object_id = ProposalObject.objects.get(name=proposal_object).id,
                author_id          = author.id,
                user_id            = request.user.id
            )

            service = build('gmail', 'v1', credentials=creds)
            message = EmailMessage()

            content = "제안자 : " + sender_email + "/n" + "제안 내용 : " + content

            message.set_content(content)

            message['To']      = author.user.email
            message['From']    = "ebsgreat7@gmail.com"
            message['Subject'] = "작가" + author.user.name + '에게 제안메일 드립니다'

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message  = {
                'raw': encoded_message
            }
            send_message = (service.users().messages().send(userId='me', body=create_message).execute())

        except HttpError as error:
            send_message = None

        return send_message
