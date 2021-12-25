from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from posts.filter import PostFilter
from posts.models import Post, Tag, Comment, Favorites, PostLike
from account.models import User
from posts.permissions import IsAdmin, IsAuthor
from posts.serializers import PostSerializer, TagSerializer, CommentSerializer, FavoritesGetSerializer, \
    FavoritesCreateSerializer, FavoritesDestroySerializer, PostLikeSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdmin]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PostFilter
    search_fields = ['title']

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['GET'], detail=True)
    def post_like(self, request, pk):
        post = self.get_object()
        post_likes = post.post_likes.all()
        serializer = PostLikeSerializer(post_likes, many=True)
        return Response(serializer.data)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdmin]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'list':
            return []
        return [IsAuthor()]


class PostLikeViewSet(ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'list':
            return []
        return [IsAuthor()]


class FavoritesListView(ListAPIView):
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesGetSerializer

    def get(self, request):
        data = request.data
        # favorites = Favorites.objects.get(user=user)
        # print(favorites)
        serializer = FavoritesGetSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # serializer.data.setdefault('favorites', favorites)
        # print(serializer.data)
        # serializer.tests(data)
        return Response(serializer.data)

    # @action(['GET'], detail=True)
    # def favorites(self, request, pk):
    #     user = self.get_object()
    #     favorites = user.favorites.all()
    #     print(favorites)
    #     serializer = FavoritesGetSerializer(favorites, many=True)
    #     return Response(serializer.data)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(**kwargs)

    # permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     data = request.data
    #     # favorites = user.favorites.all()
    #     serializer = FavoritesSerializer(data, many=True)
    #     serializer.create(data)
    #     return Response(serializer.data)


class FavoritesCreateView(CreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesCreateSerializer

    # def post(self, request):
    #     data = request.data
    #     serializer = FavoritesCreateSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.create()


class FavoritesDestroyView(DestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesDestroySerializer
