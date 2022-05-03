from django.urls import include, path
from rest_framework import routers

from api.views import PostViewSet, CommentViewSet, ThreadViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')
router.register(r'comments/(?P<parent_id>\d+)/thread',
                ThreadViewSet, basename='thread')

urlpatterns = [
    path('', include(router.urls)),
]