from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/crear/', views.crear_usuario_view, name='crear_usuario'),
    path('usuarios/listar/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
]