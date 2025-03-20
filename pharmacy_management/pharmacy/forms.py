from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    gmail = forms.EmailField(required=True, label="Gmail")

    class Meta:
        model = User
        fields = ['username', 'gmail', 'password1', 'password2']

    
    def clean_gmail(self):
        gmail = self.cleaned_data.get('gmail')
        if User.objects.filter(email=gmail).exists():
            raise forms.ValidationError("Gmail is already in use.")
        return gmail


