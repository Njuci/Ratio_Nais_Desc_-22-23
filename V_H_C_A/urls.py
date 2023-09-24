from django.urls import path
from .views import *


urlpatterns = [
    path('create_province',CreateProvince.as_view(),name="create_province"),
    path('create_ville_or_Terri',CreateVilleTerr.as_view(),name='create_ville_or_Terri'),
    path('create_certinaiss',Create_certificatNais.as_view(),name='create_certinaiss'),
    path('get_cn_per_hosp',Get_CertN_par_hopital.as_view(),name='get_cn_per_hosp')

]