from django.urls import path
from .views import *

urlpatterns = [
    path('voir_cert',Voir_stat.as_view(),name='voir_cert'),
    path('voir_cert_par_hop/<str:token>',Voir_stat_par_hop.as_view(),name='voir_cert_par_hop'),
]
