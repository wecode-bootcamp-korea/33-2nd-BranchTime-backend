from django.urls import path

from authors.views import ProposalView

urlpatterns = [
    path("/<int:author_id>", ProposalView.as_view()),
]
