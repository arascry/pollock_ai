from django import forms

class TextForm(forms.Form):
    painting_text = forms.CharField(label='text', max_length=100)