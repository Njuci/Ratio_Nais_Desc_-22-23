from django.urls import path
from .views import *

urlpatterns = [
    path('voir_cert',Voir_stat.as_view(),name='voir_cert'),
    
    path('voir_cert_date/<str:date>',Voir_stat_date.as_view(),name='voir_cert'),
    path('voir_cert_par_hop/<str:token>',Voir_stat_par_hop.as_view(),name='voir_cert_par_hop'),
    path('voir_cert_par_commune/<str:token>',Voir_stat_par_commune.as_view(),name='voir_cert_par_commune'),
]
