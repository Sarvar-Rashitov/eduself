from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Foydalanuvchi nomingiz',
            'autocomplete': 'username'
        }),
        help_text="Faqat harflar, raqamlar va @/./+/-/_ belgilaridan foydalaning."
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'email@example.com',
            'autocomplete': 'email'
        })
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Parolingiz',
            'autocomplete': 'new-password'
        }),
        help_text="Parol kamida 8 ta belgidan iborat bo'lishi va faqat raqamlardan iborat bo'lmasligi kerak."
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Parolni qayta kiriting',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu foydalanuvchi nomi allaqachon band. Boshqa nom tanlang.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro'yxatdan o'tgan. Boshqa email kiriting yoki kirish sahifasiga o'ting.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Foydalanuvchi nomingiz',
            'autocomplete': 'username'
        }),
        error_messages={
            'required': 'Foydalanuvchi nomini kiriting.'
        }
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Parolingiz',
            'autocomplete': 'current-password'
        }),
        error_messages={
            'required': 'Parolni kiriting.'
        }
    )
    
    error_messages = {
        'invalid_login': "Foydalanuvchi nomi yoki parol noto'g'ri. Qaytadan urinib ko'ring.",
        'inactive': "Bu hisob faol emas.",
    }


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ro\'yxatdan o\'tgan email'})
    )


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Yangi parol",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parol'})
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni qayta kiriting'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos kelmayapti.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Foydalanuvchi nomi',
            'email': 'Email',
            'bio': 'Bio',
            'profile_image': 'Profil rasmi',
        }
