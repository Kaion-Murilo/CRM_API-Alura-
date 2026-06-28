from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Client, Note


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        vendor_group = Group.objects.get(name='Vendedor')
        user.groups.add(vendor_group)
        return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'status', 'responsavel', 'created_at', 'updated_at']
        # ↑ adicionou 'responsavel'
        read_only_fields = ['id', 'responsavel', 'created_at', 'updated_at']
        # ↑ responsavel é read_only; a view preenche automaticamente


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['client', 'user', 'texto', 'tipo', 'data_criacao']
        # ↑ remova 'id' daqui
        read_only_fields = ['data_criacao', 'user', 'client']