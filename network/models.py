from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_posts")
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Post {self.id}: {self.content} posted by {self.author}"

    def save(self, *args, **kwargs):
    # If no timestamp is provided, use the current time
        if not self.timestamp:
            self.timestamp = timezone.now()
        super(Post, self).save(*args, **kwargs)

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
