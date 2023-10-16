# archivos/urls.py
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('cargar/', views.guardar_imagen, name='guardar_imagen'),
    path('productos/', ListaProductos.as_view(), name='lista_productos'),
    path('guardar-productos/', guardar_productos, name='guardar_productos'),
    path('borrar-productos/', borrar_productos, name='borrar_productos'),
    path('borrar-producto/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
