from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from .models import User
import re


class EmailRegisterForm(forms.ModelForm):
    """Email bilan ro'yxatdan o'tish"""
    email = forms.EmailField(
        label="Email",
        required=True,
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
        help_text="Parol kamida 8 ta belgidan iborat bo'lishi kerak."
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
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ismingiz',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Familiyangiz',
                'autocomplete': 'family-name'
            }),
        }
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email.lower()
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
        if password.isdigit():
            raise ValidationError("Parol faqat raqamlardan iborat bo'lmasligi kerak.")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Parollar mos kelmayapti.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = None  # Email bilan ro'yxatdan o'tganda telefon bo'sh
        user.set_password(self.cleaned_data['password1'])
        user.auth_provider = 'email'
        user.email_verified = False
        if commit:
            user.save()
        return user


class PhoneRegisterForm(forms.ModelForm):
    """Telefon raqam bilan ro'yxatdan o'tish"""
    phone = forms.CharField(
        label="Telefon raqam",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '+998 90 123 45 67',
            'autocomplete': 'tel'
        })
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Parolingiz',
            'autocomplete': 'new-password'
        }),
        help_text="Parol kamida 8 ta belgidan iborat bo'lishi kerak."
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
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ismingiz',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Familiyangiz',
                'autocomplete': 'family-name'
            }),
        }
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Telefon raqamni tozalash (faqat raqamlar)
        phone_digits = re.sub(r'\D', '', phone)
        
        # Agar 9 ta raqam bo'lsa, country code qo'shamiz (default +998)
        if len(phone_digits) == 9:
            phone_digits = '998' + phone_digits
        elif not phone_digits.startswith('998') and len(phone_digits) == 12:
            # Boshqa mamlakat kodi bilan kelgan bo'lsa
            pass
        elif len(phone_digits) != 12:
            raise ValidationError("Telefon raqam noto'g'ri formatda.")
        
        # Unique tekshirish
        if User.objects.filter(phone=phone_digits).exists():
            raise ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        
        return phone_digits
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
        if password.isdigit():
            raise ValidationError("Parol faqat raqamlardan iborat bo'lmasligi kerak.")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Parollar mos kelmayapti.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.email = None  # Telefon bilan ro'yxatdan o'tganda email bo'sh
        user.set_password(self.cleaned_data['password1'])
        user.auth_provider = 'phone'
        user.phone_verified = False
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Email yoki telefon bilan kirish"""
    username = forms.CharField(
        label="Email yoki Telefon",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email yoki telefon raqam',
            'autocomplete': 'username'
        }),
        error_messages={
            'required': 'Email yoki telefon raqamni kiriting.'
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
        'invalid_login': "Email/telefon yoki parol noto'g'ri.",
        'inactive': "Bu hisob faol emas.",
    }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Email yoki telefon ekanligini aniqlash
        if '@' in username:
            # Email
            return username.lower()
        else:
            # Telefon raqam - faqat raqamlarni qoldirish
            phone_digits = re.sub(r'\D', '', username)
            if not phone_digits.startswith('998') and len(phone_digits) == 9:
                phone_digits = '998' + phone_digits
            return phone_digits
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Email yoki telefon orqali foydalanuvchini topish
            user = None
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    pass
            else:
                try:
                    user = User.objects.get(phone=username)
                except User.DoesNotExist:
                    pass
            
            if user is None:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            
            if not user.check_password(password):
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            
            if not user.is_active:
                raise ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
            
            self.user_cache = user
        
        return self.cleaned_data


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
            raise ValidationError("Parollar mos kelmayapti.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "O'zingiz haqingizda..."}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
            'phone': 'Telefon',
            'bio': 'Bio',
            'profile_image': 'Profil rasmi',
        }
