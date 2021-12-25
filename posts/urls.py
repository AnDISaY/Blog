from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (PostViewSet, TagViewSet,
                    CommentViewSet, FavoritesListView, FavoritesCreateView, FavoritesDestroyView, PostLikeViewSet)


router = SimpleRouter()
router.register('post', PostViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)
# router.register('favorites_list', FavoritesListView)
router.register('post_likes', PostLikeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', FavoritesListView.as_view()),
    path('favorites/add/', FavoritesCreateView.as_view()),
    path('favorites/delete/<int:pk>/', FavoritesDestroyView.as_view()),
]
