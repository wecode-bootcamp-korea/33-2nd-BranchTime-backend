from django.urls import path

from authors.views import ProposalView, AuthorListView

urlpatterns = [
    path("/<int:author_id>", ProposalView.as_view()),
    path("/", AuthorListView.as_view())
]
