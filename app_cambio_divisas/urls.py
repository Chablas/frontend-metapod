from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.index, name='inicio'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('register/', views.registrar_usuario, name='registrar_usuario'),
    path('productos/crear', views.crear_productos, name="crear_producto"),
    path('divisas/editar/<str:abbr_primary>/<str:abbr_secondary>/', views.edit_divisas, name='editar_divisa'),
    path('productos/', views.index_productos, name="index_productos"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
]