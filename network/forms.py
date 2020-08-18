from django import forms
from .models import Post

class PostForm(forms.Form):
    post = forms.CharField(label='Post', widget=forms.Textarea)