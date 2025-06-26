from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import CustomUser
from articles.models import Comment


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','first_name','email','age',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'age',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'parent')

        widgets = {
            'parent': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }


