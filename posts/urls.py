from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (PostViewSet, TagViewSet,
                    CommentViewSet)


router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls))
]
