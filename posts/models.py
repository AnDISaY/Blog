from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    likes = models.IntegerField(blank=True, null=True)
    tag = models.ForeignKey(Tag,
                            on_delete=models.RESTRICT,
                            related_name='posts')
    image = models.ImageField(upload_to='posts',
                              null=True,
                              blank=True)
    # rating = models.SmallIntegerField(
    #     validators=[
    #         MinValueValidator(1),
    #         MaxValueValidator(5)
    #     ]
    # )

    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)  # default=datetime.now(), blank=True




