from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# Create your views here.

#create login view
def login(request):
    form = AuthenticationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})

#create register view
def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {"form": form})