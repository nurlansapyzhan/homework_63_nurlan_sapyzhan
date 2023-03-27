from django.urls import path

from posts.views import AddPostView, IndexView, CreateCommentView, LikePostView

urlpatterns = [
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>', CreateCommentView.as_view(), name='post_detail'),
    path('post/<int:pk>/like', LikePostView.as_view(), name='like'),
]
