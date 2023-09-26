from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('User.urls')),
    path('app/',include('V_H_C_A.urls')),
    path('stat/',include('statistiques.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)