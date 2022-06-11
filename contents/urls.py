from django.urls import path

from .views      import CommentUploadView, PostUploadView

urlpatterns = [
    path("/<int:post_id>/comment", CommentUploadView.as_view()),
    path("/", PostUploadView.as_view()),
    path("/media", ContentImageUploadView.as_view()), 
]
