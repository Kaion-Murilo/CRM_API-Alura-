import uuid
from django.db import models
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
    def __str__(self):
        return self.name