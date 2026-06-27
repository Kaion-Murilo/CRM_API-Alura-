from rest_framework import serializers
from .models import Client
from .models import Note

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Client
        fields = ['id', 'name', 'email', 'phone', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
class NoteSerializer(serializers.ModelSerializer):
    # Serializer completo da Nota; converte model ↔ JSON.
    
    class Meta:
        model = Note
        fields = ['id', 'client', 'user', 'texto', 'tipo', 'data_criacao']
        read_only_fields = ['id', 'data_criacao', 'user', 'client']