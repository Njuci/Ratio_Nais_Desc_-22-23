from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import qrcode
from io import BytesIO
from django.core.files import File 
from PIL import Image, ImageDraw



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
    sexe_enfant=models.CharField(max_length=1,blank=True,choices=sex_choice,null=False)
    poid_enfant=models.FloatField()
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
    url_qrcode=models.CharField(max_length=2000,null=True,blank=True)
    cod_qr=models.ImageField(upload_to="certificat_naissance",null=True,blank=True)
    
    def code_qrfound(self, *args, **kwargs):
        qr_infos= {"Certificat de Naissance N° ":self.pk,"nom":self.nom_enfant,"post_nom":self.post_nom_enfant,"prenom":self.prenom_enfant,"hopital_denom":self.hospital_id.denom}
        qr_image = qrcode.make(qr_infos)
        canvas = Image.new('RGB', (qr_image.pixel_size, qr_image.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        file_name = f'qr_code_Certinaissance-{self.hospital_id}/{self.nom_enfant}{self.post_nom_enfant}{self.prenom_enfant}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.cod_qr.save(file_name, File(buffer), save=False)
        canvas.close()
        self.url_qrcode=self.cod_qr.url
        return super(CertificatNaissance,self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f'cert{self.hospital_id}'+f'{self.id}'
    
    def get_nom(self):
        self.numero_cert=f'cert{self.hospital_id}'+f'{self.id}'
        return self.numero_cert
    class Meta:
        verbose_name='Certificat de Naissance'
        verbose_name_plural='Certificats de Naissance'
        unique_together=(('nom_enfant','post_nom_enfant','prenom_enfant','sexe_enfant','date_nais_enfant'),) #en sql cette instruction correspond à la notion des clés composites
        
class ActeNaiss(models.Model):
    certNais_id=models.OneToOneField(CertificatNaissance,on_delete=models.CASCADE)
    numeros_volume=models.CharField(max_length=15,blank=True)
    numeros_folio=models.CharField(max_length=5,blank=True,null=True)
    nom_declarant=models.CharField(max_length=120,blank=True)
    qualite_declarant=models.CharField(max_length=20,blank=True)
    profession_declarant=models.CharField(max_length=20)
    date_enregistrement=models.DateField(auto_now_add=True)
    commune=models.ForeignKey(Commune,on_delete=models.PROTECT)
    langue_redaction=models.CharField(max_length=20,blank=True)
    url_qrcode=models.CharField(max_length=2000,null=True,blank=True)
    cod_qr=models.ImageField(upload_to="acte_naissance",null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.certNais_id.nom_enfant} {self.certNais_id.post_nom_enfant}  {self.certNais_id.prenom_enfant} acte_numero {self.id}'
    
    def code_qrfound(self, *args, **kwargs):
        qr_infos= {"Acte de Naissance N° ":self.pk,"nom":self.certNais_id.nom_enfant,"post_nom":self.certNais_id.post_nom_enfant,"prenom":self.certNais_id.prenom_enfant,"hopital_denom":self.commune.denom}
        qr_image = qrcode.make(qr_infos)
        canvas = Image.new('RGB', (qr_image.pixel_size, qr_image.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        file_name = f'qr_code_Actenaissance-{self.certNais_id.hospital_id}{self.certNais_id.nom_enfant}{self.certNais_id.post_nom_enfant}{self.certNais_id.prenom_enfant}{self.pk}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.cod_qr.save(file_name, File(buffer), save=False)
        canvas.close()
        self.url_qrcode=self.cod_qr.url
        return super(ActeNaiss,self).save(*args, **kwargs)
    class Meta:
        verbose_name='Acte  de Naissance'
        verbose_name_plural='Actes de Naissance'
        
        
 
class Certificat_Desc(models.Model):
    sex_choice=(('m','Masculin'),('f','Feminin'))
    hopital_id=models.ForeignKey(Hopital,on_delete=models.PROTECT)
    medecin_traitant=models.CharField(max_length=120,blank=True)
    nom_defunt=models.CharField(max_length=40,blank=True)
    post_nom_defunt=models.CharField(max_length=40,blank=True)
    prenom_defunt=models.CharField(max_length=40,blank=True)
    sexe_defunt=models.CharField(max_length=1,blank=True,choices=sex_choice,null=False)
    lieu_naissance=models.CharField(max_length=120,blank=True)
    date_naissance_defunt=models.DateField()
    profession_defunt=models.CharField(max_length=40,blank=True)
    cause_desc=models.CharField(max_length=30,blank=True)
    date_desc=models.DateField()
    date_deliv_cert=models.DateField(auto_now_add=True)
    url_qrcode=models.CharField(max_length=2000,null=True,blank=True)
    cod_qr=models.ImageField(upload_to="certificat_desces",null=True,blank=True)
    
    def code_qrfound(self, *args, **kwargs):
        qr_infos= {"Certificat de Descès N° ":self.pk,"nom":self.nom_defunt,"post_nom":self.post_nom_defunt,"prenom":self.prenom_defunt,"hopital_denom":self.hopital_id.denom}
        qr_image = qrcode.make(qr_infos)
        canvas = Image.new('RGB', (qr_image.pixel_size, qr_image.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        file_name = f'qr_code_CertDesces-{self.hopital_id}{self.nom_defunt}{self.post_nom_defunt}{self.prenom_defunt}{self.pk}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.cod_qr.save(file_name, File(buffer), save=False)
        canvas.close()
        self.url_qrcode=self.cod_qr.url
        return super(Certificat_Desc,self).save(*args, **kwargs)
    
    class Meta:
        verbose_name='Certificat de Décès'
        verbose_name_plural='Certificats de Décès'
        unique_together=(('nom_defunt','post_nom_defunt','prenom_defunt'),)
class ActeDesc(models.Model):
    etat_civile_choice=(('m','Marié'),('c','Celibataire'))
    cert_desc_id=models.OneToOneField(Certificat_Desc,on_delete=models.CASCADE)
    numeros_volume=models.CharField(max_length=15,blank=True)
    nom_declarant=models.CharField(max_length=120,blank=True)
    qualite_declarant=models.CharField(max_length=20,blank=True)
    profession_declarant=models.CharField(max_length=20,blank=True)
    residence_principale=models.CharField(max_length=220,blank=True)
    residence_temporaire=models.CharField(max_length=220,blank=True,null=True,default=None)
    nationalite=models.CharField(max_length=40,blank=True)
    etat_civile=models.CharField(max_length=1,choices=etat_civile_choice,blank=True)
    conjoint_identite=models.CharField(max_length=120,blank=True,null=True)
    nom_complet_pere=models.CharField(max_length=120,blank=True)
    nom_complet_mere=models.CharField(max_length=120,blank=True)
    date_enregistrement=models.DateField(auto_now_add=True)
    commune=models.ForeignKey(Commune,on_delete=models.PROTECT)
    langue_redaction=models.CharField(max_length=20,blank=True)
    url_qrcode=models.CharField(max_length=2000,null=True,blank=True)
    cod_qr=models.ImageField(upload_to="acte_desc",null=True,blank=True)
    
    def code_qrfound(self, *args, **kwargs):
        qr_infos= {"Acte de Descès N° ":self.pk,"nom":self.cert_desc_id.nom_defunt,"post_nom":self.cert_desc_id.post_nom_defunt,"prenom":self.cert_desc_id.prenom_defunt,"hopital_denom":self.cert_desc_id.hopital_id.denom}
        qr_image = qrcode.make(qr_infos)
        canvas = Image.new('RGB', (qr_image.pixel_size, qr_image.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        file_name = f'qr_code_ActeDesces-{self.cert_desc_id.hopital_id}{self.cert_desc_id.nom_defunt}{self.cert_desc_id.post_nom_defunt}{self.cert_desc_id.prenom_defunt}{self.pk}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.cod_qr.save(file_name, File(buffer), save=False)
        canvas.close()
        self.url_qrcode=self.cod_qr.url
        return super(ActeDesc,self).save(*args, **kwargs)
    class Meta:
        verbose_name='Acte  de Descès'
        verbose_name_plural='Actes de Descès'
        
