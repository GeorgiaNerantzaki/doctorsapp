from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from .models import CustomUser

#here we extend the built-in user registration form
class CustomUserCreationForm(BaseUserCreationForm):
    name = forms.CharField(max_length=120)
    surname = forms.CharField(max_length=120)
    email = forms.EmailField(required=True, help_text = "Enter a valid email")
    
    class Meta:
        model = CustomUser
        fields = ['name', 'surname','username','email','password1','password2']
        
    def save(self,commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user    
            