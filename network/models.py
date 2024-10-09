from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id}: {self.content} posted by {self.author}"