import jwt

from django.conf import settings
from django.test import TestCase, Client
from unittest.mock import MagicMock, patch

from users.models import User


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
        response = client.get("/users/kakao/callback", content_type = 'application/json', **headers)
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
