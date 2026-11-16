from django.shortcuts import render, redirect

# Create your views here.
from experiencias.models import Experiencia
from django.contrib.auth.decorators import login_required



def inicio_home(request):
  experiencias_activas = Experiencia.objects.all()
  return render(
      request, 'core/inicio.html', {'experiencias': experiencias_activas}
  )

@login_required
def home_redirect(request):
    rol = getattr(request.user, 'perfil', None) and request.user.perfil.rol
    if request.user.is_superuser or rol == 'Administrador' or rol == 'Guia':
        return redirect('listar_experiencias')
    return redirect('catalogo_experiencias')