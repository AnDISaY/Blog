from django_filters import rest_framework as filters

from posts.models import Post


class PostFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['tag']
