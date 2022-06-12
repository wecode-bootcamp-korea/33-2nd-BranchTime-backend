import json
import bcrypt
import jwt

from django.test import TestCase, Client
from json        import dumps
from django.conf import settings

from .models  import Author, User, ProposalObject, Proposal
from unittest import mock
from unittest.mock import patch, MagicMock

class EmailTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = "dno06103@naver.com",
            name         = "김민정",
            thumbnail    = "저거.png",
            introduction = "블라블라블라블라",
        )

        Author.objects.create(
            id           = 1,
            introduction = "블라블라",
            career       = "블라블라블라블라",
            user_id      = 1
        )

        ProposalObject.objects.create(
            id = 1,
            name = "출판기고",
        )
        
        self.token = jwt.encode({'id':User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        Author.objects.all().delete()
        User.objects.all().delete()
        Proposal.objects.all().delete()

    @patch("authors.app.GoogleEmail")
    def test_success_proposalview_post(self, mocked_requests):
        client = Client()
        data = {
            "content"        : "블라블라",
            "sender_email"   : "dno06101@naver.com",
            "proposal_object": "출판기고"
        }
    
        headers = {"HTTP_Authorization": self.token}

        class MockedResponse:
            # def __init__(self):
            #     credentials = credentials

            def generate_token(self, file_path):
                return "<google.oauth2.credentials.Credentials object at 0x111a4ff10>"

            file_path = 'token.json'

            def send_email(self, content, author, sender_email, creds):
                return JsonResponse({"message" : "SUCCESS"}, status=200)            

            content      = "블라블라"
            sender_email = "dno06103@naver.com"
            author       = Author.objects.get(id=1)
            creds        = generate_token(self, file_path)

        access_token = headers["HTTP_Authorization"]
        payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms = settings.ALGORITHM)
        user         = User.objects.get(id = payload["id"])

        Proposal.objects.create(
            sender_email       = "dno06103@naver.com",
            content            = "블라블라",
            proposal_object_id = 1,
            author_id          = 1,
            user_id            = user.id
        )
        mocked_requests.return_value = MockedResponse()

        response = client.post('/authors/1', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.json(), {'message' : 'SUCCESS'})
        self.assertEqual(response.status_code, 201)