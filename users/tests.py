import jwt, uuid

from django.conf                    import settings
from django.test                    import TestCase, Client
from django.db                      import transaction
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db                      import transaction

from unittest.mock                  import MagicMock, patch

from contents.models                import MainCategory, SubCategory
from users.models                   import SocialAccount, User
from authors.models                 import Author



@patch('users.views.requests')
class KakaoLoginViewTest(TestCase):
    def test_success_kakao_login_new_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            status_code = 200

            def json(self):
                return  {
                        "id"          : 123456789,
                        "connected_at": "2022-06-08T08:49:09Z",
                        "properties"  : {
                            "nickname"       : "\ud55c\uad6c",
                            "profile_image"  : "http://k.kakaocdn.net/dn/csofZq/btrl57D481A/p6iWmcgoBJrHumDBktY1i1/img_640x640.jpg",
                            "thumbnail_image": "http://k.kakaocdn.net/dn/csofZq/btrl57D481A/p6iWmcgoBJrHumDBktY1i1/img_110x110.jpg"
                            }, 
                        "kakao_account": {
                            "profile_nickname_needs_agreement": False,
                            "profile_image_needs_agreement"   : False,
                            "profile"                         : {
                                "nickname"           : "\ud55c\uad6c",
                                "thumbnail_image_url": "http://k.kakaocdn.net/dn/csofZq/btrl57D481A/p6iWmcgoBJrHumDBktY1i1/img_110x110.jpg",
                                "profile_image_url"  : "http://k.kakaocdn.net/dn/csofZq/btrl57D481A/p6iWmcgoBJrHumDBktY1i1/img_640x640.jpg",
                                "is_default_image"   : False
                                }, 
                            "has_email"                       : True,
                            "email_needs_agreement"           : False,
                            "is_email_valid"                  : True,
                            "is_email_verified"               : True,
                            "email"                           : "abcd@naver.com"
                            },
                        }
                    

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers  = {"HTTP_Authoriazation": "kakao_token"}
        response = client.get("/users/kakao", content_type = 'application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'token' : jwt.encode({
                    'id' : User.objects.latest("id").id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
                    )
            }
        )

        token   = response.json()['token']
        user_id = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)['id']
        user    = User.objects.get(id=user_id)
        self.assertEqual(user.email, "abcd@naver.com")

class UserDetailViewTest(TestCase):
    def setUp(self):
        with transaction.atomic():
            User.objects.bulk_create([
                User(
                    id           = 1,
                    name         = "?????????",
                    email        = "test@gmail.com",
                    thumbnail    = "test.jpg",
                    introduction = "??????????????? BranchTime?????????."
                    ),
                User(
                    id           = 2,
                    name         = "?????????",
                    email        = "test1@gmail.com",
                    thumbnail    = "test1.jpg",
                    introduction = "??????????????? BranchTime?????????."
                    )
                ])
            SocialAccount.objects.bulk_create([
                SocialAccount(
                    id                = 1,
                    social_account_id = "123123123",
                    name              = "kakao",
                    user_id           = 1
                    ),
                SocialAccount(
                    id                = 2,
                    social_account_id = "123123456",
                    name              = "kakao",
                    user_id           = 2
                    ) 
                ])
        MainCategory.objects.create(
            id   = 1,
            name = "??????????????????"
        )
        SubCategory.objects.create(
            id              = 1,
            name            = "??????????????????",
            maincategory_id = 1
        )

        Author.objects.create(
            id             = 1,
            introduction   = "?????? ?????? ??????????????????",
            career         = "??????????????? ??????",
            user_id        = 1,
            subcategory_id = 1
        )
        self.token = jwt.encode({'id':User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()  
        Author.objects.all().delete()  
        MainCategory.objects.all().delete()  
        SubCategory.objects.all().delete()  

    def test_user_detail_view_success(self):
        client = Client()        

        headers = {"HTTP_Authorization":self.token}
        
        response = client.get('/users/mypage', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": {
                "id"              : 1,
                "name"            : "?????????",
                "description"     : "??????????????? BranchTime?????????.",
                "avatar"          : "test.jpg",
                "subscriber"      : 0,
                "interestedAuthor": 0,
                "author"          : {
                    "description": "?????? ?????? ??????????????????",
                    "career"     : "??????????????? ??????",
                    }
                }
            }
        )
    def test_user_detail_view_invalid_token(self):
        client = Client()        
        
        headers = {"HTTP_Authorization":"??????_token"}
        
        response = client.get('/users/mypage', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID TOKEN"})    

    def test_user_detail_view_invalid_user(self):
        client = Client()        
        self.token = jwt.encode({'id':3}, settings.SECRET_KEY, settings.ALGORITHM)
        headers = {"HTTP_Authorization":self.token}
        
        response = client.get('/users/mypage', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVAILD_USER"})        
