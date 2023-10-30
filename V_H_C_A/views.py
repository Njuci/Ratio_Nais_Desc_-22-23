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
    


@api_view(["GET"])
def Get_CertificatNaissPrint(request,id):
    
    
    try:
        certificat=CertificatNaissance.objects.get(id=id)
        certficatSerial=CertiNaissSerial(certificat)
        
        print(certficatSerial.data)
        ho=(certficatSerial.data['hospital_id'])
        print(type(ho))
        hosp=Hopital.objects.get(id=ho)
        hospCerial=Hopitalserial(hosp)
        prov=province.objects.get(id=hospCerial.data['prov'])
        provCerial=ProvinceSerial(prov)
        tv=TerriVille.objects.get(id=hospCerial.data['TerriVi'])
        tvCer=TerrVilleSerial(tv)
        Cert={"province":provCerial.data,"terriville":tvCer.data,"hospital":hospCerial.data,"Certificat":certficatSerial.data}
        
        
        
        print(hospCerial.data)
        
        
        
        
        return Response(Cert,status=status.HTTP_200_OK)
        
        
    except Certificat_Desc.DoesNotExist:
        
        return Response({"object":"does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
    
    
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
                    certN=CertificatNaissance.objects.get(id=cert)
                    U =certN.code_qrfound()
                    CertSeria=CertiNaissSerial(certN)                    
                    return Response({"message":"Certificat"+ f"{cert}"+" a été enregistré avec succès","data":CertSeria.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":CertSerial.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
        
    def put(self,request):
        token=request.data['token']
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        cert_id=request.data['certNaiss_id']
        cert_naissance=request.data['cert_naiss']
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                hopital=Hopital.objects.get(user=user.id)
                cert_naiss=CertificatNaissance.objects.get(id=cert_id,hospital_id=hopital.id)
                cert_naiss_serial=CertiNaissSerial(instance=cert_naiss,data=cert_naissance,partial=True)
                if cert_naiss_serial.is_valid():
                    cert_naiss_serial.save()
                    certN=CertificatNaissance.objects.get(id=cert_naiss_serial.data['id'])
                    U =certN.code_qrfound()
                    CertSeria=CertiNaissSerial(certN)              
                    
                    
                    return Response({"message":"Acte de naissance a été mis à jour avec succès","data":CertSeria.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":cert_naiss_serial.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)        
        
        
    def delete(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        cert_id=request.data.get("cert_id")
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                hopital=Hopital.objects.get(user=user.id)
                cert_naiss=CertificatNaissance.objects.get(id=cert_id,hospital_id=hopital.id)
                cert_naiss.delete()
                return Response({"message":"Certificat de naissance a été supprimé avec succès"},status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)    
        
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
                ActNaiss=ActeNaissSerial(data=act)
                if ActNaiss.is_valid():
                    ActNaiss.save()
                    act=ActNaiss.data['id']
                    acte=ActeNaiss.objects.get(id=act)
                    serial=ActeNaissSerial(acte)
                    return Response({"message":"Certificat"+ f"{act}"+" a été enregistré avec succès","data":serial.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":ActNaiss.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                print(token,388)                
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            print(token,3855)
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        act_id=request.data.get("act_id")
        act=request.data.get("actenaiss")
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                commune=Commune.objects.get(user=user.id)
                act_naiss=ActeNaiss.objects.get(id=act_id,commune=commune.id)
                act_naiss_serial=ActeNaissSerial(instance=act_naiss,data=act,partial=True)
                if act_naiss_serial.is_valid():
                    act_naiss_serial.save()
                    
                    act=act_naiss_serial.data['id']
                    acte=ActeNaiss.objects.get(id=act)
                    serial=ActeNaissSerial(acte)

                    return Response({"message":"Acte de naissance a été mis à jour avec succès","data":serial.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":act_naiss_serial.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
    def delete(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        act_id=request.data.get("act_id")
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                commune=Commune.objects.get(user=user.id)
                act_naiss=ActeNaiss.objects.get(id=act_id,commune=commune.id)
                act_naiss.delete()
                return Response({"message":"Acte de naissance a été supprimé avec succès"},status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)


         
class Get_CertN_par_hopital_token(APIView):
    def get(self,request,token,id):
        token=token
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            try:
                hptl2=Hopital.objects.get(user=user.id)
            except Hopital.DoesNotExist:
                hptl2=None
            if  is_user_authorized(user.user_type,user_type_authorized) or is_user_authorized(user.user_type,"admin"):
                try:
                    certificat=CertificatNaissance.objects.get(id=id)
                    certficatSerial=CertiNaissSerial(certificat)
                    hptl=Hopital.objects.get(id=certficatSerial.data['hospital_id'])
                    hptc=Hopitalserial(hptl)
                except CertificatNaissance.DoesNotExist:
                    return Response({"message":"ce certificat n'existe pas "},status=status.HTTP_401_UNAUTHORIZED)
                print(certificat.hospital_id)
                print(hptc['id'])
                
                
                if hptl2.id == certificat.hospital_id.id or user.user_type=="admin":                
                    hospCerial=hptc
                    prov=province.objects.get(id=hospCerial.data['prov'])
                    provCerial=ProvinceSerial(prov)
                    tv=TerriVille.objects.get(id=hospCerial.data['TerriVi'])
                    tvCer=TerrVilleSerial(tv)
                    Cert={"province":provCerial.data,"terriville":tvCer.data,"Certificat":certficatSerial.data}
                               
                    return Response(Cert,status=status.HTTP_200_OK)
                else:
                    return Response({"message":"user non aut"},status=status.HTTP_401_UNAUTHORIZED)
                    
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
                    cert_des=Certificat_Desc.objects.get(id=cert)
                    U=cert_des.code_qrfound()
                    serial=Certi_Desc_Serial(cert_des)
                    return Response({"message":"Certificat Desc"+ f"{cert}"+" a été enregistré avec succès","data":serial.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":Certdesc.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        cert_id=request.data.get("cert_id")
        cert=request.data.get("certidesc")
        user_type_authorized='hopital'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                hopital=Hopital.objects.get(user=user.id)                
                cert_desc=Certdesc.objects.get(id=cert_id,hopital_id=hopital.id)
                Certdesc=Certi_Desc_Serial(instance=cert_desc,data=cert,partial=True)
                if Certdesc.is_valid():
                    Certdesc.save()                    
                    cert=Certdesc.data['id']
                    cert_des=Certificat_Desc.objects.get(id=cert)
                    cert_des.cod_qr()
                    serial=Certi_Desc_Serial(cert_des)
                    
                    return Response({"message":"Certificat Desc a été mis à jour avec succès","data":serial.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":Certdesc.errors}
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

class Get_CertDesc_par_hopital(APIView):
    def get(self,request,token):
        token=token
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)    
        print(type(verification_token))    
        user_type_authorized='hopital'
        if verification_token[0]==True:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            try:
                hptl=Hopital.objects.get(user=user.id)
            except Hopital.DoesNotExist:
                hptl=None
            if  is_user_authorized(user.user_type,user_type_authorized):
                cert_par_hopital= Certificat_Desc.objects.filter(hopital_id=hptl.id).order_by('date_deliv_cert')
                serial=Certi_Desc_Serial(cert_par_hopital,many=True)
                return Response(serial.data,status=status.HTTP_200_OK)               
                   
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)
                
        else:
            return Response({"message":"utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)
        



        
class Get_acteNais_par_commune(APIView):
    def get(self,request,token):
        token=token
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            try:
                hptl=Commune.objects.get(user=user.id)
            except Hopital.DoesNotExist:
                hptl=None
                
            if  is_user_authorized(user.user_type,user_type_authorized):
                acte_naisscerial=ActeNaiss.objects.filter(commune_id=hptl.id).order_by('date_enregistrement')
                serial= ActeNaissSerial(acte_naisscerial,many=True)
                return Response(serial.data,status=status.HTTP_200_OK)     
                   
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)
                
        else:
            return Response({"message":"utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)        
class Create_ActeNais(APIView):
    def post(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        act=request.data.get("new_acte_desc")
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                commune=Commune.objects.get(user=user.id)
                act['commune']=commune.id
                Actdesc=Acte_Desc_Serial(data=act)
                if Actdesc.is_valid():
                    Actdesc.save()
                    act=Actdesc.data['id']
                    return Response({"message":"Certificat"+ f"{act}"+" a été enregistré avec succès","data":Actdesc.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":Actdesc.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
                
            else:
                print(token,388)                
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
                                    
        else:
            print(token,3855)
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        act_id=request.data.get("act_id")
        act=request.data.get("acte_desc")
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                commune=Commune.objects.get(user=user.id)
                act_desc=ActeDesc.objects.get(id=act_id,commune=commune.id)
                act_desc_serial=Acte_Desc_Serial(instance=act_desc,data=act,partial=True)
                if act_desc_serial.is_valid():
                    act_desc_serial.save()
                    acte=ActeDesc.objects.get(request.data['act_id'])
                    acte.code_qrfound()
                    acte_ser=Acte_Desc_Serial(acte)
                    return Response({"message":"Acte de naissance a été mis à jour avec succès","data":acte_ser.data},status=status.HTTP_201_CREATED)
                else:
                    message={"message":"les donnees sont mal envoyé","errors":act_desc_serial.errors}
                    return Response(message,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)
    def delete(self,request):
        token=request.data.get('token')
        secret_key=settings.SECRET_KEY
        verification_token=is_access_token_valid(token,secret_key)
        act_id=request.data.get("act_id")
        user_type_authorized='commune'
        if verification_token[0]:
            user=MyUser.objects.get(id=verification_token[1]['user_id'])
            if is_user_authorized(user.user_type,user_type_authorized):
                commune=Commune.objects.get(user=user.id)
                act_desc=ActeDesc.objects.get(id=act_id,commune=commune.id)
                act_desc.delete()
                return Response({"message":"Acte de desces a été supprimé avec succès"},status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"type d'utilisateur non autorisé"},status=status.HTTP_401_UNAUTHORIZED)      
        else:
            return Response({"message":"authentification échouée"},status=status.HTTP_401_UNAUTHORIZED)

