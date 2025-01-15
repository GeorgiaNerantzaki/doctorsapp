from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.

#create login view
def login_view(request):
    if request.method == "POST":
        # Bind form with POST data
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Extract username and password
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")

            # Authenticate the user
            user = authenticate(request, username=username,password=raw_password)
            print(f"Authentication result: {user}")
            if user is not None:
                if user.is_active:
                    # Log the user in
                  if check_password(raw_password, user.password):
                    login(request, user)
                    print("User is authenticated")
                    return redirect('/index')  # Redirect to home page
                else:
                    messages.error(request, "This account is inactive.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        # Render an empty form for GET request
        form = AuthenticationForm()

    return render(request, 'login.html', {"form": form})


#create register view
def register(request):
 
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if CustomUser.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if CustomUser.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('/')
    return render(request, 'register.html')

#logout view
def log_out(request):
    logout(request)
    return redirect('/')