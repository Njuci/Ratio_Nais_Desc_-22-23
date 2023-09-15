from .views import *
from .token_serializer_view  import MyTokenObtainPairView
from rest_framework_simplejwt.views import (TokenRefreshView)

from django.urls import path,include
urlpatterns = [
        path('mec/',CreateCommune.as_view()),
        path('user_token',MyTokenObtainPairView.as_view(),name='user_token'),
        path('user_token_refresh',TokenRefreshView.as_view(),name='user_token_refresh')
]
