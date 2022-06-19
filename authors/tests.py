import json
import bcrypt
import jwt

from django.test import TestCase, Client
from json        import dumps
from django.conf import settings

from users.models       import Subscription
from authors.models     import Author, User, ProposalObject, Proposal, InterestedAuthor
from contents.models    import SubCategory, MainCategory
from unittest           import mock
from unittest.mock      import patch, MagicMock

class ProposalTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = "dno06103@naver.com",
            name         = "김민정",
            thumbnail    = "저거.png",
            introduction = "블라블라블라블라",
        )

        MainCategory.objects.create(
            id   = 1,
            name = "출판"
        )

        SubCategory.objects.create(
            id              = 1,
            name            = "출판기고",
            maincategory_id = 1
        )
       
        Author.objects.create(
            id             = 1,
            introduction   = "블라블라",
            career         = "블라블라블라블라",
            user_id        = 1,
            subcategory_id = 1
        )

        ProposalObject.objects.create(
            id   = 1,
            name = "출판기고",
        )

        self.token = jwt.encode({'id':User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        Author.objects.all().delete()
        User.objects.all().delete()
        Proposal.objects.all().delete()
        ProposalObject.objects.all().delete()

    @patch("utils.google_email_api.GoogleEmail")
    def test_success_proposalview_post(self, mocked_requests):
        client = Client()

        data = {
            "content"           : "블라블라",
            "sender_email"      : "dno06101@naver.com",
            "proposal_object_id": 1
        }
        # self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization":self.token}
        
        class MockedResponse:
            def __init__(self):
                self.credentials = {}

            def generate_token(self, token_file_path, credentials_file_path):
                return None

            def send_email(self, content, author, sender_email):
                return  {'id': '181771428a3c3f2b', 'threadId': '181771428a3c3f2b', 'labelIds': ['SENT']}       

        mocked_requests.return_value = MockedResponse()
        
        response = client.post('/authors/1/proposal', json.dumps(data), content_type='application/json', **headers)
        print(response)
        self.assertEqual(response.status_code, 201)

    @patch("utils.google_email_api.GoogleEmail")
    def test_fail_proposalview_post(self, mocked_requests):
        client = Client()

        data = {
            "content"           : "블라블라",
            "sender_email"      : "dno06101@naver.com",
            "proposal_object_id": 2
        }

        self.token = jwt.encode({'id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization":self.token}
        
        class MockedResponse:
            def __init__(self):
                self.credentials = {}

            def generate_token(self, token_file_path, credentials_file_path):
                return None

            def send_email(self, content, author, sender_email):
                return  {'id': '181771428a3c3f2b', 'threadId': '181771428a3c3f2b', 'labelIds': ['SENT']}       

        mocked_requests.return_value = MockedResponse()
        
        response = client.post('/authors/1/proposal', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)

class AuthorListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = "dno06103@naver.com",
            name         = "김민정",
            thumbnail    = "저거.png",
            introduction = "블라블라블라블라",
        )

        MainCategory.objects.create(
            id   = 1,
            name = "출판"
        )

        SubCategory.objects.create(
            id              = 1,
            name            = "출판기고",
            maincategory_id = 1
        )

        Author.objects.create(
            id             = 1,
            introduction   = "블라블라",
            career         = "블라블라블라블라",
            user_id        = 1,
            subcategory_id = 1
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()
   
    def test_success_authorlistview_post(self):
        client         = Client()
        subcategory_id = 1
        response       = client.get("/authors", {'subcategory_id' : subcategory_id})

        self.assertEqual(response.json(), {
             'message': [{
                'author_thumbnail': '저거.png',
                'author_name': '김민정',
                'author_introduction': '블라블라',
                'author_subcategory': '출판기고',
                'author_id': 1}]
        })

        self.assertEqual(response.status_code, 201)

class AuthorDetailTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = "dno06103@naver.com",
            name         = "김민정",
            thumbnail    = "저거.png",
            introduction = "블라블라블라블라",
        )

        User.objects.create(
            id           = 2,
            email        = "dno06102@naver.com",
            name         = "김성준",
            thumbnail    = "요거.png",
            introduction = "블라블라블라블라",
        )

        MainCategory.objects.create(
            id   = 1,
            name = "출판"
        )

        SubCategory.objects.create(
            id              = 1,
            name            = "출판기고",
            maincategory_id = 1
        )

        Author.objects.create(
            id             = 1,
            introduction   = "블라블라",
            career         = "블라블라블라블라",
            user_id        = 1,
            subcategory_id = 1
        )

        Author.objects.create(
            id             = 2,
            introduction   = "블라블라2",
            career         = "블라블라블라블라2",
            user_id        = 2,
            subcategory_id = 1
        )

        InterestedAuthor.objects.create(
            id        = 1,
            author_id = 2,
            user_id   = 1
        )

        Subscription.objects.create(
            id                 = 1,
            subscribed_user_id = 2,
            subscriber_id      = 1
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()
   
    def test_success_authordetailview_post(self):
        client         = Client()
        subcategory_id = 1
        response       = client.get("/authors/1")
        self.assertEqual(response.json(), {
             'author_detail': {
                'id'              : 1,
                'name'            : '김민정',
                'description'     : '블라블라',
                'avatar'          : '저거.png',
                'subscriber'      : 1,
                'interestedAuthor': 1
                }
        })
        
        self.assertEqual(response.status_code, 200)

    def test_fail_authordetailview_post(self):
        client         = Client()
        subcategory_id = 1
        response       = client.get("/authors/22")
        
        self.assertEqual(response.status_code, 401)