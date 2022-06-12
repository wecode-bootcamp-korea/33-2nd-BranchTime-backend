import json
import datetime

from django.views    import View
from django.http     import JsonResponse

from    core.views          import upload_fileobj
from    my_settings         import MEDIA_URL, AWS_STORAGE_BUCKET_NAME
from    core.utils          import login_decorator
from    contents.models     import Comment

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
