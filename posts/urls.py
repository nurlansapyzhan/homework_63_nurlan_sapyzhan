from django.urls import path

from posts.views import AddPostView, IndexView

urlpatterns = [
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('', IndexView.as_view(), name='index'),
]
