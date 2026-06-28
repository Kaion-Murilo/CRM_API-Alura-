import pytest
from django.contrib.auth.models import User
from clientes.models import Client, Note

@pytest.mark.django_db
class TestClientModel:
    """Testes do model Client."""
    
    def test_criar_cliente(self):
        # Arrange → prepara os dados
        user = User.objects.create_user(username='joao', password='123')
        
        # Act → executa a ação
        cliente = Client.objects.create(
            name='Ana Costa',
            email='ana@email.com',
            phone='(84) 99999-9999',
            status='A',
            responsavel=user
        )
        
        # Assert → verifica o resultado
        assert cliente.name == 'Ana Costa'
        assert cliente.email == 'ana@email.com'
        assert cliente.responsavel == user
    
    def test_email_unico(self):
        # Email não pode se repetir
        user = User.objects.create_user(username='joao', password='123')
        
        Client.objects.create(
            name='Cliente 1',
            email='teste@email.com',
            status='A',
            responsavel=user
        )
        
        # Tenta criar com mesmo email
        with pytest.raises(Exception):  # Deve lançar erro
            Client.objects.create(
                name='Cliente 2',
                email='teste@email.com',  # ← repetido
                status='A',
                responsavel=user
            )