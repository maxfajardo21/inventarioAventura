from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cuentas.models import Perfil
from .forms import AdminCrearUsuarioForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

@login_required
def crear_usuario_view(request):
    if not request.user.is_superuser and getattr(getattr(request.user, 'perfil', None), 'rol', None) != 'Administrador':
        return redirect('listar_experiencias')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exists():
            error = "El nombre de usuario ya esta registrado. Por favor, elige otro."
        else:
            nuevo_usuario = User.objects.create_user(username=username, email=email, password=password)
            perfil, _ = Perfil.objects.get_or_create(user=nuevo_usuario)
            perfil.rol = rol
            perfil.save()

            return redirect('listar_usuarios')

    return render(request, 'inventarioAventuraApp/cuentas/formulario.html', {'error': error})

@login_required
def listar_usuarios(request):
    if not request.user.is_superuser and getattr(getattr(request.user, 'perfil', None), 'rol', None) != 'Administrador':
        return redirect('listar_experiencias')

    for u in User.objects.all():
        Perfil.objects.get_or_create(user=u)

    usuarios = User.objects.all().select_related('perfil')
    return render(request, 'inventarioAventuraApp/cuentas/listar_usuarios.html', {
        'usuarios': usuarios
    })

def eliminar_usuario(request, pk):
    usuario_a_borrar = get_object_or_404(User, pk=pk)
    if usuario_a_borrar == request.user:
        messages.error(request, " No puedes eliminar tu propia cuenta de administrador.", extra_tags='danger' )
        return redirect('listar_usuarios')
    usuario_a_borrar.delete()
    messages.success(request, "Usuario eliminado exitosamente.")
    return redirect('listar_usuarios')

@login_required
def editar_usuario(request, pk):
    if not request.user.is_superuser and getattr(getattr(request.user, 'perfil', None), 'rol', None) != 'Administrador':
        return redirect('listar_experiencias')

    usuario_obj = User.objects.filter(pk=pk).first()
    if not usuario_obj:
        return redirect('listar_usuarios')
    perfil, _ = Perfil.objects.get_or_create(user=usuario_obj)
    if request.method == 'POST':
        usuario_obj.username = request.POST.get('username')
        usuario_obj.email = request.POST.get('email')
        usuario_obj.save()
        perfil.rol = request.POST.get('rol')
        perfil.save()

        return redirect('listar_usuarios')
    return render(request, 'inventarioAventuraApp/cuentas/formulario.html', {
        'usuario_obj': usuario_obj, 
        'perfil': perfil
    })