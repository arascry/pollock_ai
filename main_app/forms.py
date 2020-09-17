from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class TextForm(forms.Form):
    painting_text = forms.CharField(label='text', max_length=100)

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']