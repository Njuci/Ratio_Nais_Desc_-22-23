from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import province, TerriVille
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import *
from rest_framework.decorators import api_view
from datetime import datetime
from django.contrib.auth import authenticate
from django.conf import settings
import jwt

def is_access_token_valid(access_token, secret_key):
    try:
        decoded_token = jwt.decode(access_token, secret_key, algorithms=['HS256'])
        expiration_time = datetime.fromtimestamp(decoded_token['exp'])
        current_time = datetime.now()

        if current_time < expiration_time:
            return True, decoded_token
        else:
            decoded_token=None
            return False,decoded_token
    except jwt.ExpiredSignatureError:
        return False


def chek_user(username):
    try:
        user= MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        user=None
    print(user)
    if user is not None:
        return False
    else:
        return True
    
@api_view(["GET"])
def get_user_by_id(request,id):
    try:
        mysur=MyUser.objects.get(id=id)
        user_data=UtilisateurSerial2(mysur)
        return Response(user_data.data,status=status.HTTP_200_OK)
    except MyUser.DoesNotExist:
        return Response({"user":"Does not Exist"},status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    def post(self, request):
        
        # Obtenir les données d'identification de la requête
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Effectuer les vérifications d'identification, par exemple avec authenticate() de Django
        if not chek_user(username=username):
            user = MyUser.objects.get(username=username)
            #authe=authenticate(username=user.username,password=user.password)
            #print(user,authe)    
            if user is not None and password ==user.password:              # Authentification réussie
                
                # Générer un jeton d'authentification pour l'utilisateur si nécessaire
                token = RefreshToken.for_user(user)
                               
                

                return Response({"user_type":user.user_type,
                                 "user_id":user.id,
                                 "access":str(token.access_token)}, status=status.HTTP_200_OK)
            else:
                # Authentification échouée
                return Response({'message': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message":"user not found"},status=status.HTTP_401_UNAUTHORIZED)
class UserCreateView(APIView):     
    def post(self, request):
        serializer = UtilisateurSerial(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def is_user_authorized(user_type,user_type_verifie):
    if user_type==user_type_verifie:
        return True
    else:
        return False
class CreateCommune(APIView):
     def post(self,request):
         valid_type_user="admin"
         
         secret_key=settings.SECRET_KEY
         token=request.data['token']
         new_user_commune=request.data['new_user_commune']
         info_commune=request.data['info_commune']
         valid_token=is_access_token_valid(token,secret_key)
         if valid_token[0]:
             print(valid_token[1])
             request_user=valid_token[1]['user_id']
             user_request=MyUser.objects.get(id=request_user)
             if is_user_authorized(user_request.user_type,valid_type_user):
                 new_user_name=new_user_commune['username']
                 user_verif=chek_user(username=new_user_name)
                 if user_verif:
                     new_user_commune['user_type']='commune'
                     serial_user=UtilisateurSerial(data=new_user_commune)
                     if serial_user.is_valid():
                         serial_user.save()
                         info_commune['user'] = serial_user.data['id']
                         serial_commune=CommuneSerial(data=info_commune)
                         if serial_commune.is_valid():
                             serial_commune.save()
                             Communedenom=serial_commune.data['denom']
                             message={"message":"la commune"+f'{Communedenom}'+" a été créee"}
                             return Response(message,status=status.HTTP_201_CREATED)
                         else:
                             erreur=serial_commune.errors
                             user=MyUser.objects.get(username=serial_user.data['username'])
                             user.delete()
                             message={"message":"les infos sont mal donnee","erreur":erreur}
                             return Response(message,status=status.HTTP_400_BAD_REQUEST)
                         
                         
                     else:
                         message={"message":"informations invalide","errreur":serial_user.errors}
                         return Response(message,status=status.HTTP_400_BAD_REQUEST)
                 
                 return Response({"message":"l' utilisateur commune existe deja"},status=status.HTTP_400_BAD_REQUEST)
                
             else:
                 message={"message":"ce type des users n'est pas autorisé à faire cette action"}            
                 return Response(message,status=status.HTTP_401_UNAUTHORIZED)
         
         
         message={"token":"invalide access_token veuillez vous authentifiez"}
         return Response(message,status=status.HTTP_401_UNAUTHORIZED)
     
     


class CreateHospital(APIView):
     def post(self,request):
         print(request.data)
         valid_type_user="admin"
         secret_key=settings.SECRET_KEY
         token=request.data['token']
         new_user_hopital=request.data['new_user_hospital']
         info_hopital=request.data['info_hospital']
         valid_token=is_access_token_valid(token,secret_key)
         if valid_token[0]:
             request_user=valid_token[1]['user_id']
             user_request=MyUser.objects.get(id=request_user)
             if is_user_authorized(user_request.user_type,valid_type_user):
                 new_user_name=new_user_hopital['username']
                 user_verif=chek_user(username=new_user_name)
                 if user_verif:
                     new_user_hopital['user_type']='hopital'
                     serial_user=UtilisateurSerial(data=new_user_hopital)
                     if serial_user.is_valid():
                         serial_user.save()
                         info_hopital['user'] = serial_user.data['id']
                         serial_hopital=Hopitalserial(data=info_hopital)
                         if serial_hopital.is_valid():
                             serial_hopital.save()
                             hospitaldenom=serial_hopital.data['denom']
                             message={"message":"l'hopital "+f'{hospitaldenom}'+" a été créee"}
                             return Response(message,status=status.HTTP_201_CREATED)
                         else:
                             erreur=serial_hopital.errors
                             user=MyUser.objects.get(username=serial_user.data['username'])
                             user.delete()
                             message={"message":"les infos sont mal donnee","erreur":erreur}
                             return Response(message,status=status.HTTP_400_BAD_REQUEST)
                         
                         
                     else:
                         message={"message":"informations invalide","errreur":serial_user.errors}
                         return Response(message,status=status.HTTP_400_BAD_REQUEST)
                 
                 return Response({"message":"l' utilisateur hosipal existe deja"},status=status.HTTP_400_BAD_REQUEST)
                
             else:
                 message={"message":"ce type des users n'est pas autorisé à faire cette action"}            
                 return Response(message,status=status.HTTP_401_UNAUTHORIZED)
         
         
         message={"token":"invalide access_token veuillez vous authentifiez"}
         return Response(message,status=status.HTTP_401_UNAUTHORIZED)