from .views import *

from django.urls import path,include
urlpatterns = [
        
        path('create_user_admin',UserCreateView.as_view(),name='create_user'),
        path('get_user_id/<int:id>',get_user_by_id,name='get_user_id'),
        path('login_user',LoginView.as_view(),name='login_viewsss'),
        path('create_commune',CreateCommune.as_view(),name='create_commune'),
        path('create_hospital',CreateHospital.as_view(),name='create_hospital')
        ]
