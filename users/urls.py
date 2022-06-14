from xml.etree.ElementInclude import include
from django.urls import path

from .views import KakaoLoginView, UserDetailView

urlpatterns = [
    path('/kakao', KakaoLoginView.as_view()),
    path('/mypage', UserDetailView.as_view()),
]
