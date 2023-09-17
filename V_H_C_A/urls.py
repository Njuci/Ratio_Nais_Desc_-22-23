from django.urls import path
from .views import *


urlpatterns = [
    path('create_province',CreateProvince.as_view(),name="create_province")
    
    
]