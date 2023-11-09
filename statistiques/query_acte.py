from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from User.serializer import *
from User.models import *
from django.contrib.auth import authenticate
from User.views import chek_user,is_access_token_valid,is_user_authorized
from itertools import groupby
from django.conf import settings
from django.db.models import Count
def ordre_croisannt(liste):
    liste_ord=[]
    for i in range(-1,len(liste)*-1-1,-1):
        
        
        liste_ord.append(liste[i])
        print(liste[i])
    
    return liste_ord


def voir_certnais_admin():
    stat=[]       
    try:                
        certificats =CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant').order_by('-date_deliv_cert').annotate(count=Count('id'))
    except CertificatNaissance.DoesNotExist:
        return Response({"message":"l'hopital n'a pas de certoificats enregistrer"})
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
def voir_cert_desc_admin():
    stat=[]       
    try:                
        certificats =Certificat_Desc.objects.values('date_deliv_cert', 'sexe_defunt').order_by('-date_deliv_cert').annotate(count=Count('id'))
    except Certificat_Desc.DoesNotExist:
        return Response({"message":"l'hopital n'a pas de certoificats enregistrer"})
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
def voir_stat_act_admin():
    stat=[]
    try:
                
        acte_naiss =ActeNaiss.objects.values('date_enregistrement', 'certNais_id__sexe_enfant').annotate(count=Count('id'))
    except ActeNaiss.DoesNotExist:
        messqage={}
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
    stat=ordre_croisannt(stat)        
    return stat
def voir_stat_act_desc_admin():
    stat=[]
    try:
                
        acte_desc =ActeDesc.objects.values('date_enregistrement', 'cert_desc_id__sexe_defunt').annotate(count=Count('id'))
    except ActeDesc.DoesNotExist:
        messqage={}
            # Triez les certificats par date
    actes_tries = sorted(acte_desc, key=lambda x: x['date_enregistrement'])

            # Groupez les certificats par date
    groupes_actes= groupby(actes_tries, key=lambda x: x['date_enregistrement'])
        
    
         # Parcourez les groupes et affichez le nombre de filles et de garçons pour chaque date
    for date_deliv_acte, groupe in groupes_actes:
        
        nombre_filles = 0
        nombre_garcons = 0
        stata={ }   
            
        for certificat in groupe:
            sexe_enfant = certificat['cert_desc_id__sexe_defunt']
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
    stat=ordre_croisannt(stat)        
    
    return stat

 
def voir_hopital_cert_naissance(token):
    stat=[]
    user_val=is_access_token_valid(token,settings.SECRET_KEY)
        
    if user_val[0]:
        user=MyUser.objects.get(id=user_val[1]['user_id'])
        if is_user_authorized('hopital',user.user_type):
                
            try:
                hpl=Hopital.objects.get(user=user)                        
                certificats = CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant', 'hospital_id').filter(hospital_id=hpl.id).annotate(count=Count('id'))
            except CertificatNaissance.DoesNotExist:
                return Response({"message":"l'hopital n'a pas de certoificats enregistrer"})
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
                        
                            
                    if sexe_enfant == 'f':
                        nombre_filles += nombre_certificats
                    elif sexe_enfant == 'm':
                        nombre_garcons += nombre_certificats
                        
                    stata['date']=date_deliv_cert
                    stata['garcon']=nombre_garcons
                    stata['fille']=nombre_filles
                    stata['total']=stata['fille']+stata['garcon']
                    stat.append(stata)
                    
                
            return Response(stat,status=status.HTTP_200_OK)
        else:
            return Response({"messge":"type_d'utilisateur invalid"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message":"utilisateur invalide"},status=status.HTTP_401_UNAUTHORIZED)
        