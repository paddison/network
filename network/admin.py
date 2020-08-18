from django.contrib import admin
from .models import User, Post, Likes, Followers

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Followers)
