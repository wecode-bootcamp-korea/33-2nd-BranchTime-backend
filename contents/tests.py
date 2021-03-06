import jwt

from django.test       import TestCase, Client
from django.conf       import settings
from django.db         import transaction

from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock     import patch, MagicMock

from users.models      import SocialAccount
from .models           import MainCategory, Post, SubCategory, User
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



class PostListViewTest(TestCase):
    def setUp(self):
        with transaction.atomic():
            User.objects.bulk_create()(
                id = 1,
                name         = "홍길동",
                email        = "test@gmail.com",
                thumbnail    = "test.jpg",
                introduction = "홍길동님의 BranchTime입니다."
            )
            SocialAccount.objects.bulk_create()(
                        id = 1,
                        social_account_id = "123123123",
                        name              = "kakao",
                        user_id           = 1
                        )
        
        MainCategory.objects.bulk_create()(
            id           = 1,
            name         = "개발 프로그래밍",
        )
        MainCategory.objects.bulk_create()(
            id           = 2,
            name         = "웹 개발",
        )
        MainCategory.objects.bulk_create(
            id           = 3,
            name         = "프론트엔드",
        )
        MainCategory.objects.bulk_create(
            id           = 4,
            name         = "백엔드",
        )
        SubCategory.objects.bulk_create(
            id              = 1,
            name            = "협업",
            maincategory_id = 1,
        )
        SubCategory.objects.bulk_create(
            id              = 2,
            name            = "메타버스",
            maincategory_id = 1,
        )
        SubCategory.objects.bulk_create(
            id              = 3,
            name            = "소프트웨어 테스트",
            maincategory_id = 1,
        )
        Post.objects.bulk_create(
            title           = "1번글 제목입니다",
            sub_title       = "1번 소제목입니다",
            thumbnail_image = "test.jpg",
            content         = "1번글 내용",
            reading_time    = "13:10",
            subcategory_id  = 1,
            user_id         = 1
            )
        Post.objects.bulk_create(
            title           = "2번글 제목입니다",
            sub_title       = "2번 소제목입니다",
            thumbnail_image = "test.jpg",
            content         = "2번글 내용",
            reading_time    = "13:10",
            subcategory_id  = 2,
            user_id         = 1
            )
        Post.objects.bulk_create(
            title           = "3번글 제목입니다",
            sub_title       = "3번 소제목입니다",
            thumbnail_image = "test.jpg",
            content         = "3번글 내용",
            reading_time    = "13:10",
            subcategory_id  = 3,
            user_id         = 1
            )

    def tearDown(self):
        MainCategory.objects.all().delete()  
        SubCategory.objects.all().delete()  
        Post.objects.all().delete()  

    def test_post_list_view_success(self):
        client = Client()        
        print(client)
        response = client.get('/contents/postlist/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            "title_list": {
                "title"    : "개발 프로그래밍",
                "sub_title": [
                    {
                        "id": 1,
                        "name": "협업"
                    },
                    {
                        "id": 2,
                        "name": "메타버스"
                    },
                    {
                        "id": 3,
                        "name": "소프트웨어 테스트"
                    }
                ]
            },
            "post_list": [
            [{
                "id": 1,
                "title": "1번글 제목입니다",
                "subTitle": "1번 소제목입니다",
                "desc": "1번글 내용",
                "commentCount": 0,
                "writeTime": "13:10:00",
                "writeUser": "홍길동",
                "imgSrc": "test.jpg"
            }],
            [{
                "id": 2,
                "title": "2번글 제목입니다",
                "subTitle": "2번 소제목입니다",
                "desc": "2번글 내용",
                "commentCount": 0,
                "writeTime": "13:10:00",
                "writeUser": "홍길동",
                "imgSrc": "test.jpg"
            }],
            [{
                "id": 3,
                "title": "3번글 제목입니다",
                "subTitle": "3번 소제목입니다",
                "desc": "3번글 내용",
                "commentCount": 0,
                "writeTime": "13:10:00",
                "writeUser": "홍길동",
                "imgSrc": "test.jpg"
            }],]})
            

    def test_user_detail_view_doesnotexist(self):
        client = Client()        
        
        response = client.get('/contents/postlist/5', content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message":"DoesNotExist"})    