# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Student

class StudentLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", 
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'})
    )


# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'})
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ingresa tu apellido'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Crea una contraseña'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'}),
        }

    # Custom email validation to ensure the email ends with @eafit.edu.co
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@eafit.edu.co'):
            raise forms.ValidationError("El correo electrónico debe terminar con @eafit.edu.co")
        return email

