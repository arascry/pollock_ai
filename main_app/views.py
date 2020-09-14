from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Painting
# Create your views here.
def home(request):
    return render(request, 'home.html')
class PaintingsList(ListView):
    model = Paintings
class PaintingsDetail(DetailView):
    model = Painting
    fields = '__all__'
