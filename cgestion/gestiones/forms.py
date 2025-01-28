from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    # Validación personalizada para el campo de correo electrónico
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    # Meta para definir los campos que se usarán
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    # Validaciones personalizadas (si es necesario)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Validar que el correo sea de dominio @bancolombia.com.co
        if not email.endswith('@bancolombia.com.co'):
            raise forms.ValidationError("El correo electrónico debe tener el dominio '@bancolombia.com.co'.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

