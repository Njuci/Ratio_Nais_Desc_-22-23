from typing import Any
from django.contrib.auth.base_user  import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
 
# class UserBase(BaseUserManager):
#     def create_user(self,username,password,**extra_fields):
#         if not username:
#             raise ValueError(_("Username oblgatoire"))
#         if not password:
#             raise ValueError(_("Password oblgatoire"))
#         user=self.model(username=username,**extra_fields)
        
#         user.set_password(password)
#         user.save()        
#         return user
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username :
            raise ValueError('The Email field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})