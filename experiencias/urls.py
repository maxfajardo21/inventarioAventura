from django.urls import path
from . import views

urlpatterns = [
    # experiencias 
    path('gestionar/', views.listar_experiencias, name='listar_experiencias'),
    path('crear/', views.crear_experiencia, name='crear_experiencia'),
    path('editar/<int:pk>/', views.editar_experiencia, name='editar_experiencia'),
    path('eliminar/<int:pk>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    path('catalogo/', views.catalogo_experiencias, name='catalogo_experiencias'),
    
    # categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    # reservas
    path('reservar/<int:experiencia_id>/', views.crear_reserva, name='crear_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reservas/todas/', views.listar_todas_reservas, name='todas_reservas'),
    path('reservas/cancelar/<int:pk>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/cambiar-pago/<int:pk>/', views.cambiar_estado_pago, name='cambiar_estado_pago'),
    
    # registro de clientes
    path('registro/', views.registro_cliente, name='registro'),
]