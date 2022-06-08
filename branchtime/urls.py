from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('authors', include('authors.urls')),
    path('contents', include('contents.urls')),
]
