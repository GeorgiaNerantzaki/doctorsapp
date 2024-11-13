from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib import messages
# Create your views here.

#create login view
def login(request):
    form = AuthenticationForm()
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not CustomUser.objects.filter(username=username).exists():
        
         messages.error(request,'Invalid username or password')
         return redirect('/')
        
        user  = authenticate(request, username=username, password = password)  
        #if user is None:
         #   messages.error(request,'User does not exist')       
        #else:
        #login(user)
        return redirect('index/')    
    return render(request, 'login.html', {"form": form})

#create register view
def register(request):
 form = CustomUserCreationForm()
 if request.method == 'POST':
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = CustomUser.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            #messages.info(request, "Username already taken!")
            messages.error(request,"User already exists")
            return redirect('/register')
        
        # Create a new User object with the provided information
        user = CustomUser.objects.create_user(
            name=first_name,
            surname=last_name,
            username=username,
            email=email
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        #messages.info(request, "Account created Successfully!")
        return redirect('/')
 return render(request, 'register.html', {"form": form})