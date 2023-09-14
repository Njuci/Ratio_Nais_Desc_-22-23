from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import province, TerriVille
#from .permssionss import admin_group


class CreateCommune(APIView):
     def get(self,request):
         from .models import Commune,MyUser
         #user=MyUser.objects.create_superuser(username="njucimech",password="mec")
         #user.groups.add(admin_group)
         #ter=TerriVille.objects.get(id=1)
         #pr=province.objects.get(id=1)
         #com=Commune.objects.create(user=user,denom="mec",prov=pr,TerriVi=ter,nom_bour='damiel')
        
         return Response({})

        


# Create your views here.
