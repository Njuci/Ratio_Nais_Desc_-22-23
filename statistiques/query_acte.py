from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from User.models import province, TerriVille
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from User.serializer import *
from User.models import *
from django.contrib.auth import authenticate
from User.views import chek_user,is_access_token_valid,is_user_authorized
from itertools import groupby


from django.db.models import Count



def voir_stat_act_admin():
    
    stat=[]
    try:
                
        acte_naiss =ActeNaiss.objects.values('date_enregistrement', 'certNais_id__sexe_enfant').annotate(count=Count('id'))
    except CertificatNaissance.DoesNotExist:
        return Response({"message":"la commune n'a pas encore enregistres d'acte de Naissance"})
            # Triez les certificats par date
    actes_tries = sorted(acte_naiss, key=lambda x: x['date_enregistrement'])

            # Groupez les certificats par date
    groupes_actes= groupby(actes_tries, key=lambda x: x['date_enregistrement'])
        
    
         # Parcourez les groupes et affichez le nombre de filles et de garçons pour chaque date
    for date_deliv_acte, groupe in groupes_actes:
        
        nombre_filles = 0
        nombre_garcons = 0
        stata={ }   
            
        for certificat in groupe:
            sexe_enfant = certificat['certNais_id__sexe_enfant']
            nombre_certificats = certificat['count']
            print(sexe_enfant,nombre_certificats)
                    
            if sexe_enfant == 'f':
                nombre_filles += nombre_certificats
            elif sexe_enfant == 'm':
                nombre_garcons += nombre_certificats
                d=+1
            stata['date']=date_deliv_acte
            stata['garçon']=nombre_garcons
            stata['fille']=nombre_filles
            stata['total']=stata['fille']+stata['garçon']
        stat.append(stata)    
    
       
    
    
    return stat