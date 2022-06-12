import json
import datetime

from django.views    import View
from django.http     import JsonResponse

from    core.views          import upload_fileobj
from    my_settings         import MEDIA_URL, AWS_STORAGE_BUCKET_NAME
from    core.utils          import login_decorator
from    contents.models     import Post, SubCategory, Comment

bucket = AWS_STORAGE_BUCKET_NAME
args   = {'ACL':'public-read'}

class CommentUploadView(View):
    @login_decorator
    def post(self, request, post_id):
        try:
            content         = request.POST["content"]
            user            = request.user
            image           = request.FILES['comment_image']

            if not str(image).split('.')[-1] in ['png', 'jpg', 'gif', 'jpeg']:
                return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)

            key = "comment_image/" + str(post_id) + "/" + str(image) 

            upload_fileobj(Fileobj=image, Bucket=bucket, Key=key, ExtraArgs=args)

            image_url = MEDIA_URL + key

            Comment.objects.create(
                content = content,
                user_id = user.id,
                image   = image_url,
                post_id = post_id
            )

            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
class PostUploadView(View):
    @login_decorator
    def post(self, request):
        try:
            content         = request.POST["content"]
            reading_time    = datetime.time(0,int(len(content.replace(" ",""))/275+1),0)
            user            = request.user
            subcategory     = request.POST["subcategory"]
            sub_title       = request.POST["sub_title"]
            thumbnail_image = request.FILES.get('thumbnail_image', None)
            color_code      = request.POST.get('color_code', None)
            title           = request.POST["title"]

            if thumbnail_image is not None:
                if not str(thumbnail_image).split('.')[-1] in ['png', 'jpg', 'gif', 'jpeg']:
                    return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)

                key = "/thumbnail_image/" + str(user.id) + "/" + str(thumbnail_image) 

                upload_fileobj(Fileobj=thumbnail_image, Bucket=bucket, Key=key, ExtraArgs=args)
                thumbnail_image = MEDIA_URL + key

            else:
                thumbnail_image = color_code

            Post.objects.create(
                content         = content,
                user_id         = user.id,
                subcategory_id  = SubCategory.objects.get(id=1).id,
                sub_title       = sub_title,
                thumbnail_image = thumbnail_image,
                title           = title,
                reading_time    = reading_time,
>>>>>>> bcf0e69 ([FEAT] 글쓰기 기능 추가)
            )

            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
