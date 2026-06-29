import pytest
from django.contrib.auth.models import User
from clientes.models import Client, Note


@pytest.mark.django_db
class TestClientModel:
    """Testes do model Client."""
    
    def test_criar_cliente_completo(self):
        """Testa criação de cliente com todos os dados."""
        user = User.objects.create_user(username='joao', password='123')
        
        cliente = Client.objects.create(
            name='Ana Costa',
            email='ana@email.com',
            phone='(84) 99999-9999',
            status='A',
            responsavel=user
        )
        
        assert cliente.name == 'Ana Costa'
        assert cliente.email == 'ana@email.com'
        assert cliente.phone == '(84) 99999-9999'
        assert cliente.status == 'A'
        assert cliente.responsavel == user
        assert cliente.id is not None  # UUID gerado
    
    def test_email_unico(self):
        """Testa que emails duplicados são rejeitados."""
        from django.db import IntegrityError
        
        user = User.objects.create_user(username='joao', password='123')
        
        Client.objects.create(
            name='Cliente 1',
            email='teste@email.com',
            status='A',
            responsavel=user
        )
        
        # Tenta criar com mesmo email
        with pytest.raises(Exception):
            Client.objects.create(
                name='Cliente 2',
                email='teste@email.com',
                status='A',
                responsavel=user
            )
    
    def test_cliente_str(self):
        """Testa representação em string do cliente."""
        user = User.objects.create_user(username='joao', password='123')
        
        cliente = Client.objects.create(
            name='Ana Costa',
            email='ana@email.com',
            status='A',
            responsavel=user
        )
        
        assert str(cliente) == 'Ana Costa - joao'
    
    def test_cliente_status_padrao(self):
        """Testa que o status padrão é 'Ativo'."""
        user = User.objects.create_user(username='joao', password='123')
        
        cliente = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            responsavel=user
        )
        
        assert cliente.status == 'A'
    
    def test_cliente_phone_opcional(self):
        """Testa que phone é opcional."""
        user = User.objects.create_user(username='joao', password='123')
        
        cliente = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        assert cliente.phone == ''
    
    def test_timestamp_criacao(self):
        """Testa que created_at é preenchido automaticamente."""
        user = User.objects.create_user(username='joao', password='123')
        
        cliente = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        assert cliente.created_at is not None
        assert cliente.updated_at is not None
    
    def test_listar_clientes(self):
        """Testa listagem de clientes."""
        user = User.objects.create_user(username='joao', password='123')
        
        Client.objects.create(name='Cliente 1', email='c1@email.com', status='A', responsavel=user)
        Client.objects.create(name='Cliente 2', email='c2@email.com', status='A', responsavel=user)
        
        clientes = Client.objects.all()
        assert clientes.count() == 2
    
    def test_deletar_cliente(self):
        """Testa deleção de cliente."""
        user = User.objects.create_user(username='joao', password='123')
        
        cliente = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        cliente_id = cliente.id
        cliente.delete()
        
        assert not Client.objects.filter(id=cliente_id).exists()


@pytest.mark.django_db
class TestNoteModel:
    """Testes do model Note."""
    
    def test_criar_nota_completa(self):
        """Testa criação de nota com todos os dados."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        nota = Note.objects.create(
            client=client,
            user=user,
            texto='Cliente potencial',
            tipo='A'
        )
        
        assert nota.client == client
        assert nota.user == user
        assert nota.texto == 'Cliente potencial'
        assert nota.tipo == 'A'
        assert nota.id is not None  # UUID gerado
    
    def test_nota_tipo_padrao(self):
        """Testa que o tipo padrão é 'Anotação'."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        nota = Note.objects.create(
            client=client,
            user=user,
            texto='Nota teste'
        )
        
        assert nota.tipo == 'A'
    
    def test_nota_str(self):
        """Testa representação em string da nota."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        nota = Note.objects.create(
            client=client,
            user=user,
            texto='Cliente potencial para upgrade'
        )
        
        assert 'Cliente' in str(nota)
        assert 'Cliente potencial' in str(nota)
    
    def test_nota_timestamp(self):
        """Testa que data_criacao é preenchida automaticamente."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        nota = Note.objects.create(
            client=client,
            user=user,
            texto='Nota teste'
        )
        
        assert nota.data_criacao is not None
    
    def test_notas_cliente(self):
        """Testa que notas são vinculadas corretamente ao cliente."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        Note.objects.create(client=client, user=user, texto='Nota 1')
        Note.objects.create(client=client, user=user, texto='Nota 2')
        
        notas = Note.objects.filter(client=client)
        assert notas.count() == 2
    
    def test_deletar_cliente_deleta_notas(self):
        """Testa que deletar cliente deleta suas notas (CASCADE)."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        nota = Note.objects.create(client=client, user=user, texto='Nota teste')
        nota_id = nota.id
        
        client.delete()
        
        assert not Note.objects.filter(id=nota_id).exists()
    
    def test_tipos_nota(self):
        """Testa todos os tipos de nota."""
        user = User.objects.create_user(username='joao', password='123')
        client = Client.objects.create(
            name='Cliente',
            email='cliente@email.com',
            status='A',
            responsavel=user
        )
        
        tipos = ['A', 'C', 'R']
        
        for tipo in tipos:
            nota = Note.objects.create(
                client=client,
                user=user,
                texto=f'Nota tipo {tipo}',
                tipo=tipo
            )
            assert nota.tipo == tipo