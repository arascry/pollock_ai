from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .painting import make_painting
from .models import Painting
from django.contrib.auth.models import User
from .forms import TextForm

import uuid
import boto3
import os
import environ

environ.Env()
environ.Env.read_env()

# Create your views here.
def home(request):
    return render(request, 'home.html')

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

def upload_painting(name, painting_img):

    if painting_img:
        s3 = boto3.client(
            's3',
            aws_access_key_id = os.environ['ACCESS_ID'],
            aws_secret_access_key = os.environ['SECRET_ID'],
        )

        key = uuid.uuid4().hex[:6] + str(name.rfind('.'))
        try:
            s3.put_object(
                Bucket=os.environ['BUCKET'],
                Key=key,
                Body=painting_img,
                ContentType='image/png'
            )

            #s3.upload_fileobj(painting_img, os.environ['BUCKET'], key)
            url = f"{os.environ['S3_BASE_URL']}{os.environ['BUCKET']}/{key}"
            return url
        except:
            print('An error occured uploading painting to S3')
            return

            
class PaintingsCreate(LoginRequiredMixin, CreateView):
    model = Painting
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.urls = [upload_painting(form.cleaned_data['name'], make_painting(form.cleaned_data['name']))]
        return super().form_valid(form)

class PaintingsList(LoginRequiredMixin, ListView):
    model = Painting
    fields = ['name']

class PaintingsDetail(LoginRequiredMixin, DetailView):
    model = Painting
    fields = '__all__'

class PaintingsUpdate(LoginRequiredMixin, UpdateView):
    model = Painting
    fields = ['name']

    def dispatch(self, request, *args, **kwargs):
        painting = Painting.objects.get(id=kwargs['pk'])
        if self.request.user == painting.user:
            return super(PaintingsUpdate, self).dispatch(request, *args, *kwargs)
        else:
            return redirect('detail', pk=kwargs['pk'])

class PaintingsDelete(LoginRequiredMixin, DeleteView):
    model = Painting
    success_url = '/paintings/'

    def dispatch(self, request, *args, **kwargs):
        painting = Painting.objects.get(id=kwargs['pk'])
        if self.request.user == painting.user:
            return super(PaintingsDelete, self).dispatch(request, *args, *kwargs)
        else:
            return redirect('detail', pk=kwargs['pk'])    

@login_required
def user_detail(request, pk):
    user = User.objects.get(id=pk)
    num_paintings = len(Painting.objects.filter(user=pk))
    return render(request, 'auth/user_detail.html', {
        'num_paintings': num_paintings
    })
