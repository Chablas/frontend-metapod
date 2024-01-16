from django.urls import path
from . import views

urlpatterns = [
    path('conversor/', views.index, name='divisas'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('register/', views.registrar_usuario, name='registrar_usuario'),
    path('divisas/crear', views.crear_divisas, name="crear_divisa"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
]