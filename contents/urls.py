from django.urls import path

from .views import CommentUploadView

urlpatterns = [
    path("/<int:post_id>/comment", CommentUploadView.as_view()),
]
