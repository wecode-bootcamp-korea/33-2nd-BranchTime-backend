import json
import bcrypt
import jwt
from io import BytesIO

from django.test       import TestCase, Client
from django.conf       import settings

from django.core.files.uploadedfile import SimpleUploadedFile

from .models           import User
from unittest          import mock
from unittest.mock     import patch, MagicMock
from core.views        import upload_fileobj
from my_settings       import MEDIA_URL

class CommentImageUploadTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = "dno06103@naver.com",
            name         = "김민정",
            thumbnail    = "저거.png",
            introduction = "블라블라블라블라",
        )

        self.token = jwt.encode({'id':User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()

    @patch("core.views.upload_fileobj")
    def test_success_comment_image_upload(self, mocked_requests):
        client = Client()

        headers = {"HTTP_Authorization": self.token}
        content_image = SimpleUploadedFile('요거.png', b'')       
       
        class MockedResponse:
            def upload_fileobj(Fileobj, Bucket, Key, ExtraArgs):
                return True

            access_token  = headers["HTTP_Authorization"]
            payload       = jwt.decode(access_token, settings.SECRET_KEY, algorithms = settings.ALGORITHM)
            user          = User.objects.get(id = payload["id"])
            content_image = 'fd.png'

            file = upload_fileobj(
                Fileobj='fd.png',
                Bucket='minjeong',
                Key="content_image/" + str(user.id) + "/" + str(content_image),
                ExtraArgs={'ACL':'public-read'}
            )

        mocked_requests.return_value = MockedResponse()
        response         = client.post('/contents/media', {'content_image' : content_image},**headers)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response,
        #     {
        #         'message' : "https://minjeong.s3.ap-northeast-2.amazonaws.com/content_image/1/"+ str(content_image)
        #     }
        # )
        