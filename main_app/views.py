from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .painting import make_painting
from .models import Painting
from .forms import TextForm

import uuid
import boto3

# Create your views here.
def home(request):
    return render(request, 'home.html', context={
        'img': make_painting().decode('utf-8')
    })

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'The information you provided is invalid. Please, try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

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

class PaintingsCreate(LoginRequiredMixin, CreateView):
    model = Painting
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.urls = ['DUMMY_URL']
        return super().form_valid(form)

class PaintingsList(LoginRequiredMixin, ListView):
    model = Painting
    fields = ['name']

class PaintingsDetail(LoginRequiredMixin, DetailView):
    model = Painting
    fields = '__all__'