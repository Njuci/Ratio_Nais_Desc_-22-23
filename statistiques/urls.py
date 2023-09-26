from django.urls import path
from .views import *

urlpatterns = [
    path('voir_cert',Voir_stat.as_view(),name='voir_cert')
]
