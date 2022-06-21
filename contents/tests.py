import jwt, json

from django.test                    import TestCase, Client
from django.conf                    import settings
from django.db                      import transaction

from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock                  import patch, MagicMock

from users.models                   import SocialAccount
from .models                        import MainCategory, Post, SubCategory, User, Comment
from utils.file_upload_api          import AWSFileUploader

class PostUploadTest(TestCase):
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

        self.token = jwt.encode({'id':User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_success_postuploadview_post(self, mocked_requests):
        client  = Client()
        headers = {"HTTP_Authorization":self.token}

        thumbnail_image = SimpleUploadedFile('요거.png', b'')
        content         = "블라블라"
        subcategory     = 1
        sub_title       = "fadsfasd"
        title           = "fa"

        class MockedResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        mocked_requests.return_value = MockedResponse()
        
        response                     = client.post('/contents',  {'thumbnail_image' : thumbnail_image, 'content' : content,\
            'subcategory' : subcategory, 'sub_title' : sub_title, 'title' : title }, **headers)
        self.assertEqual(response.status_code, 201)

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_fail_extension_postuploadview_post(self, mocked_requests):
        client  = Client()
        headers = {"HTTP_Authorization":self.token}

        thumbnail_image = SimpleUploadedFile('요거.pdf', b'')
        content         = "블라블라"
        subcategory     = 1
        sub_title       = "fadsfasd"
        title           = "fa"
        class MockedResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"

        mocked_requests.return_value = MockedResponse()
        response                     = client.post('/contents',  {'thumbnail_image' : thumbnail_image,\
             'content':content,'subcategory':subcategory, 'sub_title':sub_title, 'title':title }, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID EXTENSION"})

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_fail_key_error_postuploadview_post(self, mocked_requests):
        client  = Client()
        headers = {"HTTP_Authorization":self.token}

        thumbnail_image = SimpleUploadedFile('요거.png', b'')
        contents        = "블라블라"
        subcategory     = 1
        sub_title       = "fadsfasd"
        title           = "fa"

        class MockedResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        mocked_requests.return_value = MockedResponse()

        response = client.post('/contents',  {'thumbnail_image' : thumbnail_image, 'contents':contents,'subcategory':subcategory,
        'sub_title':sub_title, 'title':title }, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

class PostTest(TestCase):
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

        Post.objects.create(
            id              = 1,
            title           = "1번글 제목입니다",
            sub_title       = "1번 소제목입니다",
            thumbnail_image = "test.jpg",
            content         = "1번글 내용",
            reading_time    = "13:10",
            subcategory_id  = 1,
            user_id         = 1
        )
        
        Comment.objects.create(
            id        = 1,
            image     = "test.jpg",
            content   = "1번글 내용",
            post_id   = 1,
            user_id   = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()

    def test_success_comment_image_upload(self):
        client   = Client()
        response = client.get('/contents/1')

class CategoryTest(TestCase):
    def setUp(self):

        MainCategory.objects.create(
            id   = 1,
            name = "출판"
        )

        SubCategory.objects.create(
            id              = 1,
            name            = "출판기고",
            maincategory_id = 1
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()

    def test_success_category(self):
        client   = Client()
        response = client.get('/contents/category')

class ContentImageUploadTest(TestCase):
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

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_success_content_post(self, mocked_requests):
        client  = Client()
        headers = {"HTTP_Authorization" : self.token}

        content_image = SimpleUploadedFile('요거.png', b'')

        class MockedResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_requests.return_value = MockedResponse()
        response                     = client.post('/contents/medias', {'content_image': content_image}, **headers)

        self.assertEqual(response.status_code, 201)
    
    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_fail_extension_problem_content_post(self, mocked_requests):
        client  = Client()
        headers = {"HTTP_Authorization" : self.token}

        content_image = SimpleUploadedFile('요거.pdf', b'')

        class MockedResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_requests.return_value = MockedResponse()
        response                     = client.post('/contents/medias', {'content_image': content_image}, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID EXTENSION"})

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_fail_key_error_content_post(self, mocked_requests):
        client  = Client()
        headers = {"HTTP_Authorization" : self.token}

        content_images = SimpleUploadedFile('요거.pdf', b'')

        class MockedResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_requests.return_value = MockedResponse()
        response                     = client.post('/contents/medias', {'contents_images': content_images}, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

class CommentupdateTest(TestCase):
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

        Post.objects.create(
            id              = 1,
            title           = "1번글 제목입니다",
            sub_title       = "1번 소제목입니다",
            thumbnail_image = "test.jpg",
            content         = "1번글 내용",
            reading_time    = "13:10",
            subcategory_id  = 1,
            user_id         = 1
        )
        
        Comment.objects.create(
            id        = 1,
            image     = "test.jpg",
            content   = "1번글 내용",
            post_id   = 1,
            user_id   = 1
        )

        self.token = jwt.encode({'id':User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        SubCategory.objects.all().delete()
        MainCategory.objects.all().delete()
    
    @patch("utils.file_upload_api.AWSFileUploader.upload")
    @patch("utils.file_upload_api.AWSFileUploader.delete")
    def test_success_content_update(self, mocked_delete_request, mocked_upload_request):
        client  = Client()
        headers = {"HTTP_Authorization" : self.token}

        image = SimpleUploadedFile('요거.png', b'')
        content = "블라블라"

        class MockedDeleteResponse:
            def delete(self, file_name, config):
                pass
    
        class MockedUploadResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_delete_request.return_value = MockedDeleteResponse()
        mocked_upload_request.return_value = MockedUploadResponse()

        response = client.post('/contents/1/comments/1', {'image': image, 'contents':content}, **headers)
        self.assertEqual(response.status_code, 201)

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    @patch("utils.file_upload_api.AWSFileUploader.delete")
    def test_fail_extension_content_update(self, mocked_delete_request, mocked_upload_request):
        client  = Client()
        headers = {"HTTP_Authorization" : self.token}
        image   = SimpleUploadedFile('요거.pdf', b'')
        content = "블라블라"

        class MockedDeleteResponse:
            def delete(self, file_name, config):
                pass
    
        class MockedUploadResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_delete_request.return_value = MockedDeleteResponse()
        mocked_upload_request.return_value = MockedUploadResponse()

        response = client.post('/contents/1/comments/1', {'image': image, 'content':content}, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID EXTENSION"})
 
class CommentUploadTest(TestCase):
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

        Post.objects.create(
            id              = 1,
            title           = "1번글 제목입니다",
            sub_title       = "1번 소제목입니다",
            thumbnail_image = "test.jpg",
            content         = "1번글 내용",
            reading_time    = "13:10",
            subcategory_id  = 1,
            user_id         = 1
        )
        self.token = jwt.encode({'id' : User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        SubCategory.objects.all().delete()
        MainCategory.objects.all().delete()
    
    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_success_content_post(self, mocked_upload_request):
        client            = Client()
        headers           = {"HTTP_Authorization" : self.token}
        comment_image_url = SimpleUploadedFile('요거.png', b'')
        content           = "블라블라"

        class MockedUploadResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_upload_request.return_value = MockedUploadResponse()

        response = client.post('/contents/1/comments', {'comment_image_url' : comment_image_url,\
             'content' : content }, **headers)
        self.assertEqual(response.status_code, 201)

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_fail_extension_content_post(self, mocked_upload_request):
        client            = Client()
        headers           = {"HTTP_Authorization" : self.token}
        comment_image_url = SimpleUploadedFile('요거.pdf', b'')
        content           = "블라블라"

        class MockedUploadResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_upload_request.return_value = MockedUploadResponse()

        response = client.post('/contents/1/comments', {'comment_image_url' : comment_image_url,\
             'content' : content }, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID EXTENSION"})

    @patch("utils.file_upload_api.AWSFileUploader.upload")
    def test_fail_key_error_content_post(self, mocked_upload_request):
        client            = Client()
        headers           = {"HTTP_Authorization" : self.token}
        comment_image_url = SimpleUploadedFile('요거.pdf', b'')
        content           = "블라블라"

        class MockedUploadResponse:
            def upload(self, file, config, content_type):
                return "https://minjeong.s3.ap-northeast-2.amazonaws.com/thumbnail_image/060084c1-fa70-4e5b-b187-f2ca5077ab79"
        
        mocked_upload_request.return_value = MockedUploadResponse()

        response = client.post('/contents/1/comments', {'comment_image_urls' : comment_image_url,\
             'content' : content }, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

class PostListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = "dno06103@naver.com",
            name         = "김민정",
            thumbnail    = "저거.png",
            introduction = "블라블라블라블라",
        )

        MainCategory.objects.bulk_create([
            MainCategory(id = 1, name = "개발"),
            MainCategory(id = 2, name = "웹 개발"),
            MainCategory(id = 3, name = "프론트엔드"),
            MainCategory(id = 4, name = "백엔드"),
        ])

        SubCategory.objects.bulk_create([
            SubCategory(id = 1, name = "협업", maincategory_id = 1),
            SubCategory(id = 2, name = "메타버스", maincategory_id = 2),
            SubCategory(id = 3, name = "소프트", maincategory_id = 3),
        ])

        Post.objects.bulk_create([
            Post(
                title           = "1번글 제목입니다",
                sub_title       = "1번 소제목입니다",
                thumbnail_image = "test.jpg",
                content         = "1번글 내용",
                reading_time    = "13:10",
                subcategory_id  = 1,
                user_id         = 1
            ),
            Post(
                 title           = "2번글 제목입니다",
                sub_title       = "2번 소제목입니다",
                thumbnail_image = "test.jpg",
                content         = "2번글 내용",
                reading_time    = "13:10",
                subcategory_id  = 2,
                user_id         = 1
            ),
            Post(
                title           = "3번글 제목입니다",
                sub_title       = "3번 소제목입니다",
                thumbnail_image = "test.jpg",
                content         = "3번글 내용",
                reading_time    = "13:10",
                subcategory_id  = 3,
                user_id         = 1
            )
        ])

    def tearDown(self):
        MainCategory.objects.all().delete()  
        SubCategory.objects.all().delete()  
        Post.objects.all().delete()
        User.objects.all().delete()  

    def test_post_list_view_success(self):
        client = Client()    
        response = client.get('/contents/')
        self.assertEqual(response.status_code, 200)