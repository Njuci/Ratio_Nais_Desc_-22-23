from django.urls import path
from .views import *


urlpatterns = [
    path('create_province',CreateProvince.as_view(),name="create_province"),
    path('create_ville_or_Terri',CreateVilleTerr.as_view(),name='create_ville_or_Terri'),
    path('get_territoire_par_province/<int:id>',Get_Territoir_par_prov,name='get_terrtoire_par_province'),
    path('create_certinaiss',Create_certificatNais.as_view(),name='create_certinaiss'),
    path('create_actenaiss',Create_ActeNais.as_view(),name='create_actenaiss'),
    path('get_cn_per_hosp/<str:token>',Get_CertN_par_hopital.as_view(),name='get_cn_per_hosp'),
    path('get_cn_per_hosp_or_admin/<str:token>/<int:id>',Get_CertN_par_hopital_token.as_view(),name='get_cn_per_hosp'),
    path('create_certi_desc/',Create_Cert_Desc.as_view(),name='create_certi_desc'),
    path('create_actedesc',Create_ActeDesc.as_view(),name='create_actedesc'),
    path('print_cert/<int:id>',Get_CertificatNaissPrint,name='print_cert'),
    path('print_cert_desc/<int:id>',Get_CertificatDescesPrint,name='print_cert_desc'),
    path('print_acte_naiss/<int:id>',Get_Actes_Naiss_Print,name='print_acte_naiss'),
    path('print_acte_desc/<int:id>',Get_Acte_Desc_Print,name='print_acte_desc'),    
    path('get_acte_naiss_par_commune/<str:token>',Get_acteNais_par_commune.as_view(),name='get_acte_naiss_par_commune'),
    path('get_acte_desc_par_commune/<str:token>',Get_acteDesc_par_commune.as_view(),name='get_acte_desc_par_commune'),
    path("get_certi_desc_par_hopital/<str:token>",Get_CertDesc_par_hopital.as_view(),name='get_certi_desc_par_hopital')


]