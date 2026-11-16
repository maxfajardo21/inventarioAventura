from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Experiencia, Categoria, Reserva
from django.contrib.auth.forms import UserCreationForm
from cuentas.models import Perfil
from .forms import ExperienciaForm, CategoriaForm, RegistroClienteForm

@login_required
def home_redirect(request):
    if not hasattr(request.user, 'perfil'):
        return redirect('catalogo_experiencias')
    
    rol = request.user.perfil.rol
    if request.user.is_superuser or rol == 'Administrador':
        return redirect('listar_experiencias')
    elif rol == 'Guia':
        return redirect('listar_experiencias')
    else:
        return redirect('catalogo_experiencias')

@login_required
def listar_experiencias(request):
    rol = getattr(request.user, 'perfil', None) and request.user.perfil.rol
    if request.user.is_superuser or rol == 'Administrador':
        experiencias = Experiencia.objects.all()
    elif rol == 'Guia':
        experiencias = Experiencia.objects.filter(creador=request.user)
    else:
        messages.error(request, "No tienes permisos para acceder a la gestión interna.")
        return redirect('catalogo_experiencias')
    return render(request, 'inventarioAventuraApp/experiencias/listar.html', {'experiencias': experiencias})

@login_required
def crear_experiencia(request):
    rol = getattr(request.user, 'perfil', None) and request.user.perfil.rol
    es_admin_o_superuser = request.user.is_superuser or rol == 'Administrador'
    es_guia = (rol == 'Guia')
    
    if not (es_admin_o_superuser or es_guia):
        messages.error(request, "No tienes permisos para crear experiencias.")
        return redirect('listar_experiencias')
        
    if request.method == 'POST':
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            if es_guia:
                experiencia.creador = request.user
            experiencia.save()
            messages.success(request, "Experiencia creada con éxito.")
            return redirect('listar_experiencias')
    else:
        form = ExperienciaForm()
        if es_guia and 'creador' in form.fields:
            form.fields['creador'].required = False
            form.fields['creador'].widget = forms.HiddenInput()

    return render(request, 'inventarioAventuraApp/experiencias/formulario.html', {'form': form})

@login_required
def editar_experiencia(request, pk):
    rol = getattr(request.user, 'perfil', None) and request.user.perfil.rol
    es_admin_o_superuser = request.user.is_superuser or rol == 'Administrador'
    es_guia = (rol == 'Guia')
    
    if not (es_admin_o_superuser or es_guia):
        messages.error(request, "No tienes permisos para editar experiencias.")
        return redirect('listar_experiencias')
        
    experiencia = get_object_or_404(Experiencia, pk=pk)
    if rol == 'Guia' and experiencia.creador != request.user:
        messages.error(request, "No tienes permisos para editar esta experiencia.")
        return redirect('listar_experiencias')

    if request.method == 'POST':
        form = ExperienciaForm(request.POST, instance=experiencia)
        if form.is_valid():
            exp = form.save(commit=False)
            if es_guia:
                exp.creador = request.user
            exp.save()
            messages.success(request, "Experiencia actualizada correctamente.")
            return redirect('listar_experiencias')
    else:
        form = ExperienciaForm(instance=experiencia)
        if rol == 'Guia' and 'creador' in form.fields:
            form.fields['creador'].disabled = True

    return render(request, 'inventarioAventuraApp/experiencias/formulario.html', {'form': form})

@login_required
def eliminar_experiencia(request, pk):
    rol = getattr(request.user, 'perfil', None) and request.user.perfil.rol
    es_admin_o_superuser = request.user.is_superuser or rol == 'Administrador'
    
    if not (es_admin_o_superuser or rol == 'Guia'):
        messages.error(request, "No tienes permisos.")
        return redirect('listar_experiencias')
        
    experiencia = get_object_or_404(Experiencia, pk=pk)
    if not request.user.is_superuser and rol != 'Administrador':
        messages.error(request, "Acceso denegado: Los guías no pueden eliminar experiencias.")
        return redirect('listar_experiencias')

    if request.method == 'POST':
        experiencia.delete()
        messages.success(request, "Experiencia eliminada exitosamente.")
        return redirect('listar_experiencias')
        
    return render(request, 'inventarioAventuraApp/experiencias/confirmar_eliminacion.html', {'experiencia': experiencia})

@login_required
def listar_categorias(request):
    rol = request.user.perfil.rol if hasattr(request.user, 'perfil') else None
    if not request.user.is_superuser and rol != 'Administrador':
        messages.error(request, "Módulo exclusivo para Administradores.")
        return redirect('listar_experiencias')
        
    categorias = Categoria.objects.all()
    return render(request, 'inventarioAventuraApp/categorias/listar.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    rol = request.user.perfil.rol if hasattr(request.user, 'perfil') else None
    if not request.user.is_superuser and rol != 'Administrador':
        return redirect('listar_experiencias')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'inventarioAventuraApp/categorias/formulario.html', {'form': form})

def catalogo_experiencias(request):
    # Filtrar solo experiencias cuyas categorías estén activas
    experiencias = Experiencia.objects.filter(categoria__estado=True)
    return render(request, 'inventarioAventuraApp/experiencias/catalogo.html', {'experiencias': experiencias})

@login_required
def crear_reserva(request, experiencia_id):
    experiencia = get_object_or_404(Experiencia, id=experiencia_id)
    reservas_actuales = experiencia.inscripciones.count() 
    
    if reservas_actuales >= experiencia.cupo_maximo:
        messages.error(request, "¡Lo sentimos! Esta experiencia ya no cuenta con cupos disponibles.")
        return redirect('catalogo_experiencias')
        
    if request.method == 'POST':
        # Se instancia y guarda la reserva en la base de datos de verdad
        Reserva.objects.create(
            usuario=request.user,
            experiencia=experiencia,
            estado_pago='Pendiente'
        )
        messages.success(request, "¡Reserva realizada con éxito!")
        return redirect('mis_reservas')
        
    return render(request, 'inventarioAventuraApp/experiencias/formulario.html', {'experiencia': experiencia})

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'inventarioAventuraApp/inscripciones/mis_reservas.html', {'reservas': reservas})

@login_required
def listar_todas_reservas(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'Administrador':
        return redirect('listar_experiencias')
    reservas = Reserva.objects.all()
    return render(request, 'inventarioAventuraApp/experiencias/todas_reservas.html', {'reservas': reservas})

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.get_or_create(user=user, defaults={'rol': 'Turista'})
            messages.success(request, "¡Cuenta creada con éxito! Ya puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'inventarioAventuraApp/cuentas/registro.html', {'form': form})

@login_required
def editar_categoria(request, pk):
    rol = request.user.perfil.rol if hasattr(request.user, 'perfil') else None
    if not request.user.is_superuser and rol != 'Administrador':
        messages.error(request, "Acceso exclusivo para Administradores.")
        return redirect('listar_experiencias')

    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'inventarioAventuraApp/categorias/formulario.html', {'form': form})

@login_required
def eliminar_categoria(request, pk):
    rol = request.user.perfil.rol if hasattr(request.user, 'perfil') else None
    if not request.user.is_superuser and rol != 'Administrador':
        messages.error(request, "Acceso exclusivo para Administradores.")
        return redirect('listar_experiencias')

    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoría eliminada exitosamente.")
        return redirect('listar_categorias')
        
    return render(request, 'inventarioAventuraApp/categorias/confirmar_eliminacion.html', {'categoria': categoria})

@login_required
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    rol = getattr(getattr(request.user, 'perfil', None), 'rol', None)
    
    if reserva.usuario != request.user and rol != 'Administrador':
        return redirect('mis_reservas')
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva cancelada correctamente.")
        if rol == 'Administrador':
            return redirect('todas_reservas')
        return redirect('mis_reservas')
        
    return render(request, 'inventarioAventuraApp/inscripciones/confirmar_cancelacion.html', {'reserva': reserva})

@login_required
def cambiar_estado_pago(request, pk):
    rol = getattr(getattr(request.user, 'perfil', None), 'rol', None)
    if not request.user.is_superuser and rol != 'Administrador':
        return redirect('listar_experiencias')

    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        if reserva.estado_pago == 'Pendiente':
            reserva.estado_pago = 'Confirmado'
        else:
            reserva.estado_pago = 'Pendiente'
        reserva.save()
        messages.success(request, "Estado de pago actualizado.")
    return redirect('todas_reservas')