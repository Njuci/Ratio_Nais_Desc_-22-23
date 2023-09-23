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
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,Permission
class MyUser(AbstractUser):
    USER_TYPE_CHOICES = (
           ('admin', 'Admin'),
           ('commune', 'Commune'),
           ('hopital', 'Hopital'),
       )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD='username'
    groups = models.ManyToManyField(Group, related_name='myuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='myuser_set', blank=True
    )
    
    
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
    nom_bour=models.CharField(max_length=50)   
    def __str__(self) -> str:
        return self.denom
    class Meta:
        verbose_name='Commune'
        verbose_name_plural='Communes'
        
class Hopital(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    email=models.EmailField(unique=True,default="email@gmail.com")
    boite_postal=models.CharField(max_length=9,blank=True)
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
    sex_choice=(('m','Masculin'),('f','Feminin'))
    hospital_id=models.ForeignKey(Hopital,on_delete=models.PROTECT)
    nom_medecin=models.CharField(max_length=40,blank=True)
    nom_enfant=models.CharField(max_length=40,blank=True)
    post_nom_enfant=models.CharField(max_length=40,blank=True)
    prenom_enfant=models.CharField(max_length=40,blank=True)
    sexe_enfant=models.CharField(max_length=1,blank=True,choices=sex_choice)
    poid_enfant=models.FloatField(default=0.00)
    date_nais_enfant=models.DateField(auto_now_add=True)
    date_deliv_cert=models.DateField(auto_now=True)
    nom_complet_pere=models.CharField(max_length=120,blank=True)
    profession_pere=models.CharField(max_length=20,blank=True)
    date_nais_pere=models.DateField()
    lieu_nais_pere=models.CharField(max_length=20,blank=True)
    nationalite_pere=models.CharField(max_length=20,blank=True)    
    nom_complet_mere=models.CharField(max_length=120,blank=True)
    profession_mere=models.CharField(max_length=20,blank=True)
    date_nais_mere=models.DateField()
    lieu_nais_mere=models.CharField(max_length=20,blank=True)
    nationalite_mere=models.CharField(max_length=20)
    localite_parent=models.CharField(max_length=20,blank=True)
    collectiv_parent=models.CharField(max_length=20,blank=True)
    def __str__(self) -> str:
        return f'cert{self.hospital_id}'+self.id
    
    def get_nom(self) -> str:
        return f'cert{self.hospital_id}'+self.id
    class Meta:
        verbose_name='Certificat de Naissance'
        verbose_name_plural='Certificats de Naissance'
        
        
class ActeNaiss(models.Model):
    certNais_id=models.OneToOneField(CertificatNaissance,on_delete=models.CASCADE)
    numeros_volume=models.CharField(max_length=5,blank=True)
    numeros_folio=models.CharField(max_length=5,blank=True,null=True)
    nom_declarant=models.CharField(max_length=120)
    qualie_declarant=models.CharField(max_length=20,blank=True)
    profession_declarant=models.CharField(max_length=20)
    date_enregitrement=models.DateField(auto_now_add=True)
    commune=models.ForeignKey(Commune,on_delete=models.PROTECT)
    langue_redaction=models.CharField(max_length=20,blank=True)
    

    