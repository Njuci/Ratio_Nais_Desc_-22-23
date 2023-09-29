from django.urls import path
from .views import *


urlpatterns = [
    path('create_province',CreateProvince.as_view(),name="create_province"),
    path('create_ville_or_Terri',CreateVilleTerr.as_view(),name='create_ville_or_Terri'),
    path('get_territoire_par_province/<int:id>',Get_Territoir_par_prov,name='get_terrtoire_par_province'),
    path('create_certinaiss',Create_certificatNais.as_view(),name='create_certinaiss'),
    path('get_cn_per_hosp/<str:token>',Get_CertN_par_hopital.as_view(),name='get_cn_per_hosp'),

]