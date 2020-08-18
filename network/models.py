from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea



class User(AbstractUser):
    def __str__(self):
        return self.username.capitalize()

    def liked(self, post_id):
        if Likes.objects.get(user=self.id, post=post_id):
            return True
        else:
            return False

    def get_followers(self):
        return Followers.objects.filter(user=self.id).count()

    def get_following(self):
        return Followers.objects.filter(follower=self.id).count()

    def check_follows(self, id):
        try:
            Followers.objects.get(user=id, follower=self.id)
            return True
        except:
            return False

class Post(models.Model):
    text = models.CharField(max_length=280)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Post by {self.user}"

    def get_likes(self):
        return Likes.objects.filter(post=self.id).count()

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower} follows {self.user}"

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {
            'text': 'New Post'
        }
        widgets = {
            'text': Textarea(attrs={'class': 'new-post-field', 'placeholder': 'New Post'})
        }