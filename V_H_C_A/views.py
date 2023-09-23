from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from User.models import province, TerriVille
from rest_framework.response import Response
from rest_framework import status
from User.serializer import *
from User.models import *
from django.contrib.auth import authenticate
from User.views import chek_user,is_access_token_valid,is_user_authorized
class CreateProvince(APIView):
    def post(self,request):
        serial=ProvinceSerial(data=request.data)
        print(request.user)
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
        
        
    def get(self,request):
        cert=CertificatNaissance.objects.all().order_by('id')
        serial=CertiNaissSerial(cert,many=True)
        
        
        return Response(serial.data,status=status.HTTP_200_OK)