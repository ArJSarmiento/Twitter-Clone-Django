from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    upload = models.FileField(upload_to='media/')

DEFAULT_POST_ID = 1
class Post(models.Model):
    caption = models.CharField(max_length=255) 
    datetime = models.DateTimeField(default=now, blank=True) 
    poster = models.ForeignKey(User,default=DEFAULT_POST_ID, on_delete=models.CASCADE, related_name="poster")
    likes =   models.ManyToManyField(User, blank=True, related_name="likes")
    def __str__(self):
        return f"{self.caption}"
    
DEFAULT_FOLLOWER_ID = 1
class Followers(models.Model):
    me =  models.ForeignKey(User,default=DEFAULT_FOLLOWER_ID, on_delete=models.CASCADE, related_name="me")
    my_following =   models.ManyToManyField(User, blank=True, related_name="my_following")

    def __str__(self):
        return f"{self.me}"