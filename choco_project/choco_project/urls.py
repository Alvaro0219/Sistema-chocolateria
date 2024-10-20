from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='login'),  # Redirige a login al inicio
    path('', include('core.urls')), 
    path('productos/', include('productos.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('empleados/', include('empleados.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)