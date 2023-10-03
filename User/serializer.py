from rest_framework.serializers import ModelSerializer
from .models import *


#user serializer

class UtilisateurSerial(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
#commune       
class ProvinceSerial(ModelSerializer):
    class Meta:
        model=province
        fields="__all__"
class TerrVilleSerial(ModelSerializer):
    class Meta:
        model=TerriVille
        fields="__all__"    

class CommuneSerial(ModelSerializer):
    class Meta:
        model= Commune
        fields="__all__"
        
class Hopitalserial(ModelSerializer):
        class Meta:
            model= Hopital
            fields="__all__"
class ActeNaissSerial(ModelSerializer):
    class Meta:
        model= ActeNaiss
        fields='__all__'
        
class CertiNaissSerial(ModelSerializer):
    class Meta:
        model= CertificatNaissance
        fields="__all__"
        def get_nom(self,obj):
            return obj.get_nom()
        
        
class Certi_Desc_Serial(ModelSerializer):
    class Meta:
        model=Certificat_Desc
        fields='__all__'