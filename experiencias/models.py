from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='experiencias')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias_creadas')
    
    def __str__(self):
        return f'{self.titulo} ({self.fecha_hora.strftime("%d/%m/%Y %H:%M")})'

class Reserva(models.Model):
    ESTADOS_PAGO = (
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
    )

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservas'
    )
    experiencia = models.ForeignKey(
        Experiencia, on_delete=models.CASCADE, related_name='inscripciones'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(
        max_length=20, choices=ESTADOS_PAGO, default='Pendiente'
    )

    def __str__(self):
        return f'Reserva #{self.id} - {self.usuario.username} en {self.experiencia.titulo} [{self.estado_pago}]'