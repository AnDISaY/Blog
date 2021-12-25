from django.contrib import admin
from .models import Post, Tag, Comment, Favorites

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Favorites)

