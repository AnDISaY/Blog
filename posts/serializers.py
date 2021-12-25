from rest_framework import serializers

from account.models import User
from posts.models import Post, Tag, Comment, Favorites


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tag', 'image', 'created_at']

    # def validate_rating(self, rating):
    #     if rating not in range(1, 6):
    #         raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
    #     return rating


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text', 'rating', 'created_at']

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)


#
# class FavoritesSerializer(serializers.Serializer):
#     class Meta:
#         model = Favorites
#         fields = '__all__'
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Пользователь не найден')
#         return email
#
#     def validate_fav(self, validated_data):
#         user = self.context['request'].user
#         validated_data['user'] = user
#         favorites = user.objects.filter(user=user)
#         return favorites


# def create(self, validated_data):
#     user = self.context['request'].user
#     validated_data['favorites_user'] = user
#     return super().create(validated_data)


class FavoritesGetSerializer(serializers.Serializer):
    user = serializers.EmailField(required=True)

    def validate_user(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        user = attrs.get('user')
        favorites_queryset = Favorites.objects.filter(user=user)
        favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        attrs['user'] = favorites
        return attrs

    # def validate(self, attrs):
    #     # print(attrs)
    #     user = attrs.get('user')
    #     favorites = Favorites.objects.get(user=user)
    #     attrs['favorites'] = favorites
    #     print(favorites)
    #     return attrs

    # def validate(self, attrs):

    # def validate(self, attrs):
    #     user = self.context.get('request').user
    #     # print(self.validated_data)
    #     print(attrs)
    #     # print(user)
    #     favorites_queryset = Favorites.objects.get(user=user)
    #     # favorites = favorites_queryset.get('Favorites')
    #     # favorites = favorites_queryset[:]
    #     # user_object = Favorites.user
    #     print(favorites_queryset)
    #     # favorites = user_object.objects.filter(user=user)
    #     attrs[0] = favorites_queryset
    #     # print(len(favorites_queryset))
    #     # print(self.validated_data)
    #     print(attrs)
    #     return attrs

    # def tests(self, attrs):
    #     favorites = self.validate(attrs)
    #     print(self.validated_data)
    #     self.validated_data['post'] = favorites
    #     # print(self.validated_data)
    #     return self.validated_data

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     validated_data['user'] = user
    #     return super().create(validated_data)


class FavoritesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_post(self, post):
        if not Post.objects.filter(title=post).exists():
            raise serializers.ValidationError('Такого поста не существует')
        return post

    def validate(self, attrs):
        user = attrs.get('user')
        post = attrs.get('post')
        favorites_queryset = Favorites.objects.filter(user=user)
        favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        if str(post) in favorites:
            raise serializers.ValidationError('Вы уже добавили пост в избранное')
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class FavoritesDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'
