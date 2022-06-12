import json

from django.views    import View
from django.http     import JsonResponse

from googleapiclient.errors         import HttpError
from core.utils                     import login_decorator
from authors.models                 import Author, Proposal, ProposalObject
from google.oauth2.credentials      import Credentials
from authors.app                    import GoogleEmail

class ProposalView(View):
    @login_decorator
    def post(self, request, author_id):
        try:
            data            = json.loads(request.body)
            content         = data["content"]
            sender_email    = data["sender_email"]
            proposal_object = data["proposal_object"]
            author          = Author.objects.get(id=author_id)
            google_email = GoogleEmail(credentials="credentials.json")
            creds        = google_email.generate_token(file_path="token.json")
            google_email.send_email(content = content, author = author, sender_email = sender_email, creds=creds)
           
            Proposal.objects.create(
                sender_email       = sender_email,
                content            = content,
                proposal_object_id = ProposalObject.objects.get(name=proposal_object).id,
                author_id          = author.id,
                user_id            = request.user.id
            )
        except HttpError as error:
            send_message = None

        return JsonResponse({"message" : "SUCCESS"}, status=201)