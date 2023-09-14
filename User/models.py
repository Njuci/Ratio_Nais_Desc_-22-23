from django.db import models
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin,User
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



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

class MyUser(AbstractUser):
    username=models.CharField(max_length=50,unique=True,blank=True)
    password=models.CharField(max_length=50,blank=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='myuser'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='myuser'
    )
    REQUIRED_FIELDS=['password']
    USERNAME_FIELD = 'username'
    
    objects=CustomUserManager()
    def has_perm(self,perms):
        return True
    def has_module_perms(self,app_label):
        return True 
    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
class Commune(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    denom=models.CharField(max_length=70,blank=True)
    prov=models.ForeignKey(province,on_delete=models.PROTECT)
    TerriVi=models.ForeignKey(TerriVille,on_delete=models.PROTECT) 
    nom_bour=models.CharField(max_length=9)   
    def __str__(self) -> str:
        return self.denom
    class Meta:
        verbose_name='Commune'
        verbose_name_plural='Communes'
        
class Hopital(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    email=models.EmailField(unique=True,default="email@gmail.com")
    denom=models.CharField(max_length=70,blank=True)
    prov=models.ForeignKey(province,on_delete=models.PROTECT)
    TerriVi=models.ForeignKey(TerriVille,on_delete=models.PROTECT) 
    numeros_id=models.CharField(max_length=40,unique=True)   
    def __str__(self) -> str:
        return self.denom
    class Meta:
        verbose_name='Hopital'
        verbose_name_plural='Hopitaux'
 
class CertificatNaissance(models.Model):
    hospital_id=models.ForeignKey(Hopital,on_delete=models.PROTECT)
    