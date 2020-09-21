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
from .forms import TextForm, SignupForm

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
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'The information you provided is invalid. Please, try again.'
    form = SignupForm()
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
    def get(self, request, *args, **kwargs):
        avatar = Painting.objects.filter(user=request.user.id).last()
        avatar_url = None
        if avatar:
            avatar_url = avatar.urls[0]
        context = locals()
        context['object_list'] = Painting.objects.all()
        context['avatar_url'] = avatar_url
        return render(request, 'main_app/painting_form.html', context)
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.urls = [upload_painting(form.cleaned_data['name'], make_painting(form.cleaned_data['name']))]
        return super().form_valid(form)

class PaintingsList(LoginRequiredMixin, ListView):
    model = Painting
    fields = ['name']

    def get(self, request, *args, **kwargs):
        avatar = Painting.objects.filter(user=request.user.id).last()
        avatar_url = None
        if avatar:
            avatar_url = avatar.urls[0]
        # commissioner = User.objects.get(id=)
        context = locals()
        context['object_list'] = Painting.objects.all()
        context['avatar_url'] = avatar_url
        return render(request, 'main_app/painting_list.html', context)

    def dispatch(self, request, *args, **kwargs):
        return super(PaintingsList, self).dispatch(request, *args, **kwargs)
        

class PaintingsDetail(LoginRequiredMixin, DetailView):
    model = Painting
    fields = '__all__'
    def get(self, request, *args, **kwargs):
        avatar = Painting.objects.filter(user=request.user.id).last()
        avatar_url = None
        if avatar:
            avatar_url = avatar.urls[0]
        painting = Painting.objects.get(id=kwargs['pk'])
        context = locals()
        context['painting'] = painting
        context['avatar_url'] = avatar_url
        return render(request, 'main_app/painting_detail.html', context)

class PaintingsUpdate(LoginRequiredMixin, UpdateView):
    model = Painting
    fields = ['name']
    def get(self, request, *args, **kwargs):
        avatar = Painting.objects.filter(user=request.user.id).last()
        avatar_url = avatar.urls[0]
        context = locals()
        context['avatar_url'] = avatar_url
        return render(request, 'main_app/painting_form.html', context)
    def dispatch(self, request, *args, **kwargs):
        painting = Painting.objects.get(pk=kwargs['pk'])
        if self.request.user == painting.user:
            return super(PaintingsUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('detail', pk=kwargs['pk'])

class PaintingsDelete(LoginRequiredMixin, DeleteView):
    model = Painting
    success_url = '/paintings/'
    # pk_url_kwarg = (locals()['args'])[0]
    def get(self, request, *args, **kwargs):
        painting = Painting.objects.get(id=kwargs['pk'])
        avatar = Painting.objects.filter(user=request.user.id).last()
        avatar_url = avatar.urls[0]
        context = locals()
        # context['object'] = Painting.objects.get(id=(locals()['args'])[0])
        print('locals only:', locals())
        context['avatar_url'] = avatar_url
        context['painting'] = painting
        return render(request, 'main_app/painting_confirm_delete.html', context)
    def dispatch(self, request, *args, **kwargs):
        painting = Painting.objects.get(id=kwargs['pk'])
        context = locals()
        if self.request.user == painting.user:
            return super(PaintingsDelete, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('index')    

@login_required
def user_detail(request, pk):
    user = User.objects.get(id=pk)
    paintings = Painting.objects.filter(user=pk)
    avatar = Painting.objects.filter(user=pk).last()
    avatar_url = avatar.urls[0]
    num_paintings = len(Painting.objects.filter(user=pk))
    print("yooooo", request.user.id, 'avatar', avatar) 
    return render(request, 'auth/user_detail.html', {
        'num_paintings': num_paintings,
        'paintings': paintings,
        'avatar_url': avatar_url
    })