from rest_framework.views import APIView
from rest_framework.response import Response
from User.models import province, TerriVille
from rest_framework.response import Response
from rest_framework import status
from User.serializer import *
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
    
class Create_certificat(APIView):
    def post(self,request):
        token=request.data.get('token')
        verification_token=is_access_token_valid(token)
        user_type_authorized='hopital'
        if verification_token[0]:
            
            
            pass
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
        
        
        return 0
           
