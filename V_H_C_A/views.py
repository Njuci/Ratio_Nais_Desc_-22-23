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
class CreateProvince(APIView):
    def post(self,request):
        print(request.data)
        serial=ProvinceSerial(data=request.data)
        print()
        if serial.is_valid():
            serial.save()
            message={'message':'province créée avec succès'}
            prov=province.objects.all().order_by('denom')
            serial=ProvinceSerial(prov,many=True)
            return Response(serial.data,status=status.HTTP_201_CREATED)
        prov=request.data.get('denom')
        provt=province.objects.get(denom=prov)
        if provt is not None:
            message={'message':'il se pourrait que cette province soit deja créée'}
            return Response(message,status=status.HTTP_406_NOT_ACCEPTABLE)
        message={'message':'province non creee verofier la stracture de vos donnees'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        prov=province.objects.all().order_by('denom')
        serial=ProvinceSerial(prov,many=True)
        return Response(serial.data,status=status.HTTP_200_OK)
@api_view(["GET"])
def Get_Territoir_par_prov(request,id):
    province_id=id
    try:
        Terr=TerriVille.objects.filter(prov=province_id)
        serial=TerrVilleSerial(Terr,many=True)
    except TerriVille.DoesNotExist:
        return Response({"message":"provice id invalid"},status=status.HTTP_400_BAD_REQUEST)
        
    return Response(serial.data,status=status.HTTP_200_OK)
    
class CreateVilleTerr(APIView):
    def post(self,request):
        serial=TerrVilleSerial(data=request.data)
        if serial.is_valid():
            serial.save()
            message={'message':'La ville ou le territoire créé avec succès'}
            vte=TerriVille.objects.all().order_by('denom')
            serial=TerrVilleSerial(vte ,many=True)
            return Response(serial.data,status=status.HTTP_201_CREATED)
        Vit=request.data.get('denom')
        vt=province.objects.get(denom=Vit)
        if vt is not None:
            message={'message':'il se pourrait que cette ville ou territoire soit deja créée'}
            return Response(message,status=status.HTTP_406_NOT_ACCEPTABLE)
        message={'message':'Ville ou territoire non creee verofier la stracture de vos donnees'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        vte=TerriVille.objects.all().order_by('denom')
        serial=TerrVilleSerial(vte ,many=True)
        return Response(serial.data,status=status.HTTP_200_OK)
    
class Create_certificatNais(APIView):
    def post(self,request):
        print(request.data)
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        cert=request.data.get("new_certinaiss")
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                hopital=Hopital.objects.get(user=user.id)
                cert['hospital_id']=hopital.id
                CertSerial=CertiNaissSerial(data=cert)
                if CertSerial.is_valid():
                    CertSerial.save()
                    cert=CertSerial.data['id']
                    return Response({"message":"Certificat"+ f"{cert}"+" a été enregistré avec succès","data":CertSerial.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":CertSerial.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
        
    def put(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        cert=request.data.get("new_certinaiss")
        user_type_authorized='hopital'
                
        
        return 0    
        
        
class Create_ActeNais(APIView):
    def post(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        act=request.data.get("new_actenaiss")
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                commune=Commune.objects.get(user=user.id)
                act['commune']=commune.id
                ActNaiss=CertiNaissSerial(data=act)
                if ActNaiss.is_valid():
                    ActNaiss.save()
                    act=ActNaiss.data['id']
                    return Response({"message":"Certificat"+ f"{act}"+" a été enregistré avec succès","data":ActNaiss.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":ActNaiss.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
        
        
        

    
class Get_CertN_par_hopital(APIView):
    def get(self,request,token):
        token=token
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            try:
                hptl=Hopital.objects.get(user=user.id)
            except Hopital.DoesNotExist:
                hptl=None
            if  is_user_authorized(user.user_type,user_type_authorized):
                cert_par_hopital= CertificatNaissance.objects.filter(hospital_id=hptl.id).order_by('date_deliv_cert')
                serial=CertiNaissSerial(cert_par_hopital,many=True)
                return Response(serial.data,status=status.HTTP_200_OK)               
                   
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)
                
        else:
            return Response({"message":"utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)
           
            
            
class Create_Cert_Desc(APIView):
    def post(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        cert=request.data.get("new_certidesc")
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                hopital=Hopital.objects.get(user=user.id)
                cert['hopital_id']=hopital.id
                Certdesc=Certi_Desc_Serial(data=cert)
                if Certdesc.is_valid():
                    Certdesc.save()
                    cert=Certdesc.data['id']
                    return Response({"message":"Certificat Desc"+ f"{cert}"+" a été enregistré avec succès","data":Certdesc.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":Certdesc.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
    