from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import province, TerriVille
from .perni import commune_group


class CreateCommune(APIView):
     def get(self,request):
         from .models import Commune,MyUser
         user=MyUser.objects.create_superuser(username="njucimech",password="mec",user_type='commune')
         #user.groups.add(commune_group)
        
         return Response({'user':user.username})

        


# Create your views here.
