from django.urls import path

from .views import (
    CommentUploadView,
    CommentView,
    ContentImageUploadView,
    PostUploadView,
    PostView,
    CategoryView,
    PostListView
)

urlpatterns = [
    path("", PostUploadView.as_view()),
    path("/", PostListView.as_view()),
    path("/medias", ContentImageUploadView.as_view()),
    path("/categories", CategoryView.as_view()),
    path("/<int:post_id>", PostView.as_view()),
    path("/<int:post_id>/comments", CommentUploadView.as_view()),
    path("/<int:post_id>/comments/<int:comment_id>", CommentView.as_view()),
]
