from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from User.models import province, TerriVille
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .query_acte import voir_stat_act_admin
from rest_framework import status
from User.serializer import *
from User.models import *
from django.contrib.auth import authenticate
from User.views import chek_user,is_access_token_valid,is_user_authorized
from itertools import groupby


from django.db.models import Count

class Voir_stat(APIView):
    def get(self,request):      
        
        stat=[]
       
        try:
                
            certificats =CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant').annotate(count=Count('id'))
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
                d=+1
                stata['date']=date_deliv_cert
                stata['garçon']=nombre_garcons
                stata['fille']=nombre_filles
                stata['total']=stata['fille']+stata['garçon']
            stat.append(stata)
        data={"cert":stat,"acte_naiss":voir_stat_act_admin()}
        return Response(data,status=status.HTTP_200_OK)
    
class Voir_stat_par_hop(APIView):
    # Utilisez la méthode "annotate" sur le modèle "CertificatNaissance" pour obtenir le nombre de certificats en fonction des dates et du sexe
    def get(self,request,token):
        
        
        certificats_par_date_et_sexe = CertificatNaissance.objects.values('date_deliv_cert', 'sexe_enfant').annotate(count=Count('id'))
        stat=[]
        user_val=is_access_token_valid(token,settings.SECRET_KEY)
        
        # Parcourez les résultats pour afficher le nombre de certificats enregistrés pour chaque date et sexe
        # Obtenez tous les certificats groupés par date, sexe et hôpital
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
        
        