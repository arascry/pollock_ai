from .painting import make_painting
from django.shortcuts import render, redirect

from .forms import TextForm

# Create your views here.
def home(request):
    return render(request, 'home.html', context={
        'img': make_painting().decode('utf-8')
    })

def add_text(request):
    form = TextForm(request.POST)
    error = 'Blah'
    if form.is_valid():
        form = form.cleaned_data['painting_text']
        return render(request, 'home.html', context={
            'img': make_painting(form).decode('utf-8'),
            'text_form': form
    })
    return render(request, 'home.html', context={
        'img': make_painting().decode('utf-8'),
        'error': error
    })