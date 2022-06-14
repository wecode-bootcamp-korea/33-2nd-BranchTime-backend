import json
import datetime

from django.views           import View
from django.http            import JsonResponse
from django.db.models.query import QuerySet
from django.shortcuts       import get_object_or_404

from    core.views          import upload_fileobj
from    my_settings         import MEDIA_URL, AWS_STORAGE_BUCKET_NAME
from    botocore.exceptions import ClientError
from    core.utils          import login_decorator
from    contents.models     import Post, SubCategory, User, Comment, PostLike
import  boto3

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
            )

            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class PostView(View):
    def get(self, request, post_id):
        try:
            results = []
            post = Post.objects.prefetch_related('postlike_set','comment_set').select_related('user','subcategory').get(id = post_id)
            comments = post.comment_set.all()
            comment = [{
                'user_name'      : comment.user.name,
                'comment_image'  : comment.image,
                'comment_content': comment.content,
            } for comment in comments]
            
            results.append({
                'comment_information'    : comment,
                'post_title'             : post.title,
                'post_subtitle'          : post.sub_title,
                'post_subcategory_name'  : post.subcategory.name,
                'post_user_name'         : post.user.name,
                'post_created_at'        : post.created_at.strftime("%b.%d.%Y"),
                'post_content'           : post.content,
                'post_like_count'        : post.postlike_set.count(),
                'post_thumbnail_image'   : post.thumbnail_image,
                'user_name'              : post.user.name,
                'user_thumbnail'         : post.user.thumbnail,
                'user_introduction'      : post.user.introduction,
                'user_subscription_count': post.user.subscription.all().count()
            })

            return JsonResponse({'message' : results }, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class ContentImageUploadView(View):
    @login_decorator
    def post(self, request):
        try:
            content_image = request.FILES['content_image']
            print(content_image)
            if not str(content_image).split('.')[-1] in ['png', 'jpg', 'gif', 'jpeg']:
                return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)

            key = "content_image/" + str(request.user.id) + "/" + str(content_image)

            upload_fileobj(Fileobj=content_image, Bucket=bucket, Key=key, ExtraArgs=args)

            bucket_object_name = MEDIA_URL + key
            
            return JsonResponse({'message' : bucket_object_name}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request, comment_id):
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()

            return JsonResponse({'message' : "SUCCESS"}, status=204)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)



