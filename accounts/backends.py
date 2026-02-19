from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


class EmailPhoneBackend(ModelBackend):
    """
    Email yoki telefon raqam bilan authentication
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Email yoki telefon orqali foydalanuvchini topish
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(phone=username)
        except User.DoesNotExist:
            # Timing attack oldini olish uchun
            User().set_password(password)
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
