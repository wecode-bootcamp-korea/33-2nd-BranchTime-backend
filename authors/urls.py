from django.urls import path

from .app import ProposalView

urlpatterns = [
    path("/<int:author_id>", ProposalView.as_view()),
]
