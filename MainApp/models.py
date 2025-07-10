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

class Tag(models.Model):
    name = models.CharField(max_length=20)

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

   def __repr__(self):
       return f"C: {self.text[:10]} author:{self.author} sn: {self.snippet.name}"
