from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (PostViewSet, TagViewSet,
                    CommentViewSet, UpdatePostView)


router = SimpleRouter()
router.register('post', PostViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('update/<int:pk>/', UpdatePostView.as_view())
]
