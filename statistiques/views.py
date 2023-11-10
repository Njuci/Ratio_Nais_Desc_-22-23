from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from User.models import province, TerriVille
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .query_acte import (voir_stat_act_naiss_admin,voir_certnais_admin,voir_stat_act_desc_admin,voir_cert_desc_admin,voir_certnais_admin_date,
                         voir_cert_desc_admin_date)
from rest_framework import status
from User.serializer import *
from User.models import *
from django.contrib.auth import authenticate
from User.views import chek_user,is_access_token_valid,is_user_authorized
from itertools import groupby
from .test_liste import voir_certnais_hopital as voir_cert_naiss_par_hop

from django.db.models import Count

class Voir_stat(APIView):
    def get(self,request):    
        
        data={"cert_naissance":voir_certnais_admin(),"acte_naiss":voir_stat_act_naiss_admin(),"cert_desc":voir_cert_desc_admin(),"acte_desc":voir_stat_act_desc_admin()}
        return Response(data,status=status.HTTP_200_OK)
class Voir_stat_date(APIView):
    def get(self,request,date):    
        
        data={"cert_naissance":voir_certnais_admin_date(date),"cert_desc":voir_cert_desc_admin_date(date)}
        return Response(data,status=status.HTTP_200_OK)
    
class Voir_stat_par_hop(APIView):
    # Utilisez la méthode "annotate" sur le modèle "CertificatNaissance" pour obtenir le nombre de certificats en fonction des dates et du sexe
    def get(self,request,token):
               
        
        user_val=is_access_token_valid(token,settings.SECRET_KEY)
        
        if user_val[0]:
            user=MyUser.objects.get(id=user_val[1]['user_id'])
            if is_user_authorized('hopital',user.user_type):
                hpl=Hopital.objects.get(user=user) 
                cert_naiss=voir_cert_naiss_par_hop(hpl.id)
                return Response({"cert_naissance":cert_naiss},status=status.HTTP_200_OK)
            else:
                return Response({"message":"type d'utilisateur non autorisé "},status=status.HTTP_401_UNAUTHORIZED)
            
            
            
        return Response({"message":"invalide token"},status=status.HTTP_401_UNAUTHORIZED)