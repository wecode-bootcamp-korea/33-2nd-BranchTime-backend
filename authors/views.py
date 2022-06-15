import json

from django.views    import View
from django.http     import JsonResponse

from googleapiclient.errors         import HttpError
from core.utils                     import login_decorator
from authors.models                 import Author, Proposal, ProposalObject
from contents.models                import SubCategory
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

class AuthorListView(View):
    def get(self, request):
        try:
            
            subcategory_id = request.GET.get("subcategory_id")
            subcategory    = SubCategory.objects.get(id = subcategory_id)
            authors        = Author.objects.select_related('user').filter(subcategory_id = subcategory.id)
            
            result = [{
                "author_thumbnail"   : author.user.thumbnail,
                'author_name'        : author.user.name,
                "author_introduction": author.introduction,
                "author_subcategory" : author.subcategory.name,
                "author_id"          : author.id
            }for author in authors]

            return JsonResponse({"message" : result}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
