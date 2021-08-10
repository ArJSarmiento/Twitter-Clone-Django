from django.contrib import admin

# Register your models here.
from .models import Post, User, Followers

# Register your models here.
admin.site.register(Followers)
admin.site.register(Post)
admin.site.register(User)