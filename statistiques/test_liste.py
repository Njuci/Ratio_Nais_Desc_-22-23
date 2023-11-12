from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from User.serializer import *
from User.models import *
from django.contrib.auth import authenticate
from itertools import groupby
from django.conf import settings
from django.db.models import Count
from .query_acte import ordre_croisannt

def voir_certnais_hopital(r:int):
    stat=[]       
    certificats = CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant', 'hospital_id').filter(hospital_id=r).annotate(count=Count('id'))
            # Triez les certificats par date
    certificats_tries = sorted(certificats, key=lambda x: x['date_deliv_cert'])

            # Groupez les certificats par date
    groupes_certificats = groupby(certificats_tries, key=lambda x: x['date_deliv_cert'])
        
    print(certificats_tries)
            # Parcourez les groupes et affichez le nombre de filles et de garçons pour chaque date
    for date_deliv_cert, groupe in groupes_certificats:
        print(date_deliv_cert)
        nombre_filles = 0
        nombre_garcons = 0
        stata={ }   
            
        for certificat in groupe:
            sexe_enfant = certificat['sexe_enfant']
            nombre_certificats = certificat['count']
            print(sexe_enfant,nombre_certificats)
                    
            if sexe_enfant == 'f':
                nombre_filles += nombre_certificats
            elif sexe_enfant == 'm':
                nombre_garcons += nombre_certificats
            
            stata['date']=date_deliv_cert
            stata['garçon']=nombre_garcons
            stata['fille']=nombre_filles
            stata['total']=stata['fille']+stata['garçon']
        stat.append(stata)
    stat=ordre_croisannt(stat)    
    return stat
def voir_certnais_hopital_date(hopid:int,date:str):
    stat=[]       
    certificats = CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant', 'hospital_id').filter(hospital_id=hopid,date_deliv_cert=date).annotate(count=Count('id'))
            # Triez les certificats par date
    certificats_tries = sorted(certificats, key=lambda x: x['date_deliv_cert'])

            # Groupez les certificats par date
    groupes_certificats = groupby(certificats_tries, key=lambda x: x['date_deliv_cert'])
        
    print(certificats_tries)
            # Parcourez les groupes et affichez le nombre de filles et de garçons pour chaque date
    for date_deliv_cert, groupe in groupes_certificats:
        print(date_deliv_cert)
        nombre_filles = 0
        nombre_garcons = 0
        stata={ }   
            
        for certificat in groupe:
            sexe_enfant = certificat['sexe_enfant']
            nombre_certificats = certificat['count']
            print(sexe_enfant,nombre_certificats)
                    
            if sexe_enfant == 'f':
                nombre_filles += nombre_certificats
            elif sexe_enfant == 'm':
                nombre_garcons += nombre_certificats
            
            stata['date']=date_deliv_cert
            stata['garçon']=nombre_garcons
            stata['fille']=nombre_filles
            stata['total']=stata['fille']+stata['garçon']
        stat.append(stata)
    stat=ordre_croisannt(stat)    
    return stat





def voir_certdesc_hopital(hopid:int):
    stat=[]       
    certificats = CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant', 'hospital_id').filter(hospital_id=hopid).annotate(count=Count('id'))
            # Triez les certificats par date
    certificats_tries = sorted(certificats, key=lambda x: x['date_deliv_cert'])

            # Groupez les certificats par date
    groupes_certificats = groupby(certificats_tries, key=lambda x: x['date_deliv_cert'])
        
    print(certificats_tries)
            # Parcourez les groupes et affichez le nombre de filles et de garçons pour chaque date
    for date_deliv_cert, groupe in groupes_certificats:
        print(date_deliv_cert)
        nombre_filles = 0
        nombre_garcons = 0
        stata={ }   
            
        for certificat in groupe:
            sexe_enfant = certificat['sexe_enfant']
            nombre_certificats = certificat['count']
            print(sexe_enfant,nombre_certificats)
                    
            if sexe_enfant == 'f':
                nombre_filles += nombre_certificats
            elif sexe_enfant == 'm':
                nombre_garcons += nombre_certificats
            
            stata['date']=date_deliv_cert
            stata['garçon']=nombre_garcons
            stata['fille']=nombre_filles
            stata['total']=stata['fille']+stata['garçon']
        stat.append(stata)
    stat=ordre_croisannt(stat)    
    return stat