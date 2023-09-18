from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import province, TerriVille
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import *
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        print(request.data)
        # Obtenir les données d'identification de la requête
        username = request.data.get('username')
        password = request.data.get('password')

        # Effectuer les vérifications d'identification, par exemple avec authenticate() de Django
        user = MyUser.objects.get(username=username)
        authe=authenticate(username=user.username,password=user.password)
        print(user,authe)    
        if user is not None and password ==user.password:
            # Authentification réussie
            
            # Générer un jeton d'authentification pour l'utilisateur si nécessaire
            token = RefreshToken.for_user(user)

            return Response({'refreshToken':str(token),
                             "acccess":str(token.access_token)}, status=status.HTTP_200_OK)
        else:
            # Authentification échouée
            return Response({'message': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

class UserCreateView(APIView):
    #permission_classes = [IsAuthenticated]  # Assurez-vous que seul un utilisateur authentifié peut accéder à cette vue
    print(ModelSerializer)  
    def post(self, request):
        serializer = UtilisateurSerial(data=request.data)
        
        if serializer.is_valid():
            user=MyUser.objects.create()
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateCommune(APIView):
     def post(self,request):
         from django.conf import settings
         import jwt
         token=request.data.get('token') 
         print(token)
         scret=settings.SECRET_KEY
         decode=jwt.decode(token,scret,algorithms=['HS256'])
         
         #je prend d'abord les parametre de 
         
         nombre_user=MyUser.objects.count()
         
         
        #  user_admin_request=request.data.get('user_admin')
        #  print(user_admin_request)
        #  user_name_admin=user_admin_request.get('username')
        #  print(str(user_name_admin))
        #  user_name_admin=str(user_name_admin)
        #  user_admin_verifier= MyUser.objects.get(username=user_name_admin)
               
         return Response({'user':nombre_user,'admin':decode.keys()})

        


# Create your views here.
