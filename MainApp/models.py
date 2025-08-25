from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


LANG_CHOICES = [
    ("python", "Python"),
    ("cpp", "C++"),
    ("java", "Java"),
    ("javascript", "JavaScript")
]

LANG_ICONS = {
    "python": "fa-python",
    "cpp": "fa-c++",
    "java": "fa-java",
    "javascript": "fa-js"
}

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Tag: {self.name}"

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICES)
    code = models.TextField(max_length=5000)
    description = models.TextField(default="", blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    tags = models.ManyToManyField(to=Tag)

    def __repr__(self):
        return f"S: {self.name}|{self.lang} views:{self.views_count} public:{self.public} user:{self.user}"


class Comment(models.Model):
   text = models.TextField()
   creation_date = models.DateTimeField(auto_now_add=True)
   author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
   snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name="comments")
   likes = GenericRelation(LikeDislike)

   def __repr__(self):
       return f"C: {self.text[:10]} author:{self.author} sn: {self.snippet.name}"

   def likes_count(self):
       return self.likes.filter(vote=LikeDislike.LIKE).count()

   def dislikes_count(self):
       return self.likes.filter(vote=LikeDislike.DISLIKE).count()


from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('comment', 'Новый комментарий'),
        ('like', 'Новый лайк'),
        ('follow', 'Новый подписчик'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Уведомление для {self.recipient.username}: {self.title}"


class SnippetSubscription(models.Model):
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'snippet']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.snippet.name}"
