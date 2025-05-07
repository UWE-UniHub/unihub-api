from django.urls import path
from comments.views import comment_detail, post_comments
from .views import get_edit_delete_posts, get_put_delete_post_img, get_post_delete_post_likes

urlpatterns = [
    path('/<str:id>', get_edit_delete_posts, name='get_edit_delete_posts'),
    path('/<str:id>/img', get_put_delete_post_img, name='get_put_delete_post_img'),
    path('/<str:id>/likes', get_post_delete_post_likes, name='get_post_delete_post_likes'),
    path('/<str:post_id>/comments', post_comments, name='post-comments'),
    path('/<str:post_id>/comments/<str:comment_id>', comment_detail, name='comment-detail'),
]