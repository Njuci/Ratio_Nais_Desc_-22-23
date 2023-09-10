from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import province, TerriVille


class CreateCommune(APIView):
    pass 
    # def get(self,request):
    #     from .models import Commune,MyUser
    #     user=MyUser.objects.create_user(username="www",password="mec")
    #     ter=TerriVille.objects.get(id=1)
    #     pr=province.objects.get(id=1)
    #     com=Commune.objects.create(user=user,denom="mec",prov=pr,TerriVi=ter,nom_bour='damiel')
        
    #     return Response(com.denom)

        


# Create your views here.
