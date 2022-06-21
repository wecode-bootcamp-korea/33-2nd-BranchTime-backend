import json, datetime, requests, boto3, uuid

from django.views           import View
from django.http            import JsonResponse
from django.shortcuts       import get_object_or_404
from django.db.models       import Q

from utils.file_upload_api  import AWS_S3_function, FileHandler
from utils.login_decorator  import login_decorator
from branchtime.settings    import AWS_STORAGE_BUCKET_NAME
from contents.models        import Post, SubCategory, User, Comment, PostLike, MainCategory

file_uploader = AWS_S3_function(boto3.client('s3'))
file_handler  = FileHandler(file_uploader)

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

            if thumbnail_image :
                if not str(thumbnail_image).split('.')[-1].lower() in ['png', 'jpg', 'gif', 'jpeg']:
                    return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)

                else:
                    thumbnail_image = file_handler.upload(file = thumbnail_image, \
                        config = AWS_STORAGE_BUCKET_NAME, content_type = "thumbnail_image")
            else:
                thumbnail_image = color_code

            Post.objects.create(
                content         = content,
                user_id         = user.id,
                subcategory_id  = SubCategory.objects.get(id=subcategory).id,
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
        
        post    = Post.objects.prefetch_related('postlike_set','comment_set').\
            select_related('user','subcategory').get(id = post_id)
        comments = post.comment_set.all()

        comment = [{
            'comment_id'     : comment.id,
            'user_name'      : comment.user.name,
            'comment_image'  : comment.image,
            'comment_content': comment.content,
            
        } for comment in comments]
        
        results=[{
            'comment_information'    : comment,
            'post_id'                : post.id,
            'post_title'             : post.title,
            'post_subtitle'          : post.sub_title,
            'post_subcategory_name'  : post.subcategory.name,
            'post_user_name'         : post.user.name,
            'post_created_at'        : post.created_at.strftime("%b.%d.%Y"),
            'post_content'           : post.content,
            'post_like_count'        : post.postlike_set.count(),
            'post_thumbnail_image'   : post.thumbnail_image,
            'user_id'                : post.user.id,
            'user_name'              : post.user.name,
            'user_thumbnail'         : post.user.thumbnail,
            'user_introduction'      : post.user.introduction,
            'user_subscription_count': post.user.subscription.all().count(),
        }]

        return JsonResponse({'message' : results}, status=200)

class CategoryView(View):
    def get(self, request):
        
        categories = MainCategory.objects.all().prefetch_related('subcategory_set')

        results = [{
            'id'  : category.id,
            'main_category_name': category.name,
            'sub_category' : [{
                'id'  : subcategory.id,
                'name': subcategory.name
            }for subcategory in category.subcategory_set.all()]
        } for category in  categories]

        return JsonResponse({'message' : results}, status=200)

class ContentImageUploadView(View):
    @login_decorator
    def post(self, request):
        try:
            content_image = request.FILES['content_image']

            if not str(content_image).split('.')[-1].lower() in ['png', 'jpg', 'gif', 'jpeg']:
                    return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)
            content_image_url =file_handler.upload(content_image, AWS_STORAGE_BUCKET_NAME, "content_image")
    
            return JsonResponse({'message' : content_image_url.__str__()}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class CommentUploadView(View):
    @login_decorator
    def post(self, request, post_id):
        try:
            content         = request.POST['content']
            image           = request.FILES['comment_image_url']
            user            = request.user
       
            if not str(image).split('.')[-1].lower() in ['png', 'jpg', 'gif', 'jpeg']:
                return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)

            image_url = file_handler.upload(image, AWS_STORAGE_BUCKET_NAME, "comment_image")

            Comment.objects.create(
                content = content,
                user_id = user.id,
                image   = image_url,
                post_id = post_id
            )

            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class CommentView(View):
    @login_decorator
    def post(self, request, comment_id, post_id):

        content = request.POST.get('content', None)
        image   = request.FILES.get('image', None)
        comment = get_object_or_404(Comment, id=comment_id)

        if image is not None:
            file_id = comment.image.split("amazonaws.com/")[-1]
            file_handler.delete(file_id, AWS_STORAGE_BUCKET_NAME)

            if not str(image).split('.')[-1].lower() in ['png', 'jpg', 'gif', 'jpeg']:
                return JsonResponse({"message" : "INVALID EXTENSION"}, status=400)

            image_url     = file_handler.upload(image, AWS_STORAGE_BUCKET_NAME, "comment_image")
            comment.image = image_url

        if content:
            comment.content = content
        comment.save()
        return JsonResponse({'message' : "SUCCESS"}, status=201)

    @login_decorator
    def delete(self, request, comment_id):
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()

            return JsonResponse({'message' : "SUCCESS"}, status=204)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class PostListView(View):
    def get(self, request):
        try:
            maincategory_id = request.GET.get('maincategory')
            subcategory_id  = request.GET.get('subcategory')

            q=Q()
            if maincategory_id:
                q &= Q(subcategory__maincategory_id= maincategory_id)

            if subcategory_id:
                q &= Q(subcategory__id= subcategory_id)

            posts =Post.objects.filter(q).select_related('subcategory', 'user').order_by("-id")

            result = [{
                "maincategory_id": post.subcategory.maincategory_id,
                "subcategory_id" : post.subcategory_id,
                "post_id"        : post.id,
                "post_title"     : post.title,
                "post_subTitle"  : post.sub_title,
                "desc"           : post.content,
                "commentCount"   : post.comment_set.all().count(),
                "writeTime"      : post.created_at.strftime("%b.%d.%Y"),
                "writeUser"      : post.user.name,
                "imgSrc"         : post.thumbnail_image,
                } for post in posts]
                    
            return JsonResponse({'result' : result}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
