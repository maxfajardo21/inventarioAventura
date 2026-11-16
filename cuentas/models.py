from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
  ROLES = (
      ('Administrador', 'Administrador'),
      ('Guia', 'Guia / Operador'),
      ('Turista', 'Turista / Cliente'),
  )

  user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name='perfil'
  )
  rol = models.CharField(max_length=30, choices=ROLES, default='Turista')
  telefono = models.CharField(max_length=20, blank=True, null=True)

  def __str__(self):
    return f'{self.user.username} - {self.get_rol_display()}'


@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
  if created:
    Perfil.objects.create(user=instance)
  instance.perfil.save()