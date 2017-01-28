from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from posts.models import Feed

class WritePostForm(forms.ModelForm):
    post = forms.CharField(label="", 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Write caption here...',}),
        max_length=255, required=True)
    class Meta:
        fields = ('post',)
        model = Feed
