from django.urls import path

from authors.views import ProposalView, AuthorListView, AuthorDetailView

urlpatterns = [
    path("", AuthorListView.as_view()),
    path("/<int:author_id>", AuthorDetailView.as_view()),
    path("/<int:author_id>/proposals", ProposalView.as_view()),
]
