import uuid
from django.db import models

from django.contrib.auth.models import User
class Client(models.Model):
    NIVEL = (
        ('A', 'Ativo'),
        ('I', 'Inativo'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=1, choices=NIVEL, blank=False, null=False, default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # ↑ adicione null=True, blank=True
    
    def __str__(self):
        return f"{self.name} - {self.responsavel.username}"


class Note(models.Model):
    TIPO = (
        ('A', 'Anotação'),
        ('C', 'Contato'),
        ('R', 'Reunião'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.CharField(max_length=500)
    tipo = models.CharField(max_length=1, choices=TIPO, blank=False, null=False, default='A')
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client.name} - {self.texto[:30]}"