import uuid
from django.db import models

from django.contrib.auth.models import User
class Client(models.Model):
    StatusChoices = (
        ('L','Lead'),
        ('A','Ativo'),
        ('I','Inativo'),
    ) 
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name       = models.CharField(max_length=255)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, blank=True)
    status     = models.CharField(max_length=20, choices=StatusChoices, default="I")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    # ForeignKey → cada cliente é responsabilidade de um usuário (vendedor).
    # CASCADE → se deletar o usuário, os clientes dele também são deletados.

    def __str__(self):
        return self.name
class Note(models.Model):
    TIPO = (
        ('A', 'Anotação'),
        ('C', 'Contato'),
        ('R', 'Reunião'),
    )
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # ForeignKey → vincula a nota a um cliente; CASCADE deleta notas se cliente for removido.
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Qual usuário criou a nota.
    
    texto = models.CharField(max_length=500)
    # CharField → texto da nota; máximo 500 caracteres.
    
    tipo = models.CharField(max_length=1, choices=TIPO, blank=False, null=False, default='A')
    # Tipo de nota: Anotação, Contato ou Reunião.
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True → preenchida automaticamente na criação; nunca alterada.
    
    def __str__(self):
        return f"{self.client.name} - {self.texto[:30]}"
        # __str__ → mostra nome do cliente + primeiros 30 caracteres da nota.