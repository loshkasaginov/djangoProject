from django import forms
from django.contrib.auth.models import User
from .models import Profile, Review


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'city', 'country')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Оставьте ваш отзыв здесь...'}),
        }
