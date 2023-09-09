from django.db import models
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin,User
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone



#from .management_role import UserBase
# Create your models here.
class province(models.Model):
    denom=models.CharField(max_length=70,unique=True)
    def __str__(self) -> str:
        return self.denom

    class Meta:
        verbose_name='Province'
        verbose_name_plural='Provinces'
class TerriVille(models.Model):
    denom=models.CharField(max_length=70,unique=True)
    prov=models.ForeignKey(province,on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.denom

    class Meta:
        verbose_name='Ville ou Territoire'
        verbose_name_plural='Villes ou Territoires'
from .management_role import CustomUserManager
class MyUser(AbstractBaseUser):
    username=models.CharField(max_length=50,unique=True,blank=True)
    password=models.CharField(max_length=50,blank=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    REQUIRED_FIELDS=['password']
    USERNAME_FIELD = 'username'
    objects=CustomUserManager()
    def has_module_perms(self):
        return True
class Commune(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    denom=models.CharField(max_length=70,blank=True)
    prov=models.ForeignKey(province,on_delete=models.PROTECT)
    TerriVi=models.ForeignKey(TerriVille,on_delete=models.PROTECT) 
    nom_bour=models.CharField(max_length=9)   
    
