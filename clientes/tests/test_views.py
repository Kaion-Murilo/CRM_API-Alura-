import pytest
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status
from clientes.models import Client, Note


@pytest.mark.django_db
class TestClientViewSet:
    """Testes dos endpoints de clientes."""
    
    def setup_method(self):
        # Rode antes de cada teste
        self.client = APIClient()
        
        # Cria grupos
        self.admin_group, _ = Group.objects.get_or_create(name='Administrador')
        self.vendor_group, _ = Group.objects.get_or_create(name='Vendedor')
        
        # Cria usuários
        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@test.com'
        )
        self.admin_user.groups.add(self.admin_group)
        
        self.vendor1 = User.objects.create_user(
            username='joao', password='joao123'
        )
        self.vendor1.groups.add(self.vendor_group)
        
        self.vendor2 = User.objects.create_user(
            username='maria', password='maria123'
        )
        self.vendor2.groups.add(self.vendor_group)

    # ────────────────────────────────────────────────────
    # TESTES DE AUTENTICAÇÃO
    # ────────────────────────────────────────────────────
    
    def test_login_valido(self):
        """Testa se login com credenciais válidas retorna token."""
        response = self.client.post('/api/token/', {
            'username': 'admin',
            'password': 'admin123'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalido(self):
        """Testa se login com senha errada falha."""
        response = self.client.post('/api/token/', {
            'username': 'admin',
            'password': 'senhaerrada'
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_acesso_sem_autenticacao(self):
        """Testa se endpoints protegidos bloqueiam sem token."""
        response = self.client.get('/api/clientes/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

    # ────────────────────────────────────────────────────
    # TESTES DE CADASTRO DE CLIENTES
    # ────────────────────────────────────────────────────
    
    def test_criar_cliente_valido(self):
        """Testa criação de cliente com dados válidos."""
        self.client.force_authenticate(user=self.vendor1)
        
        response = self.client.post('/api/clientes/', {
            'name': 'Cliente Teste',
            'email': 'cliente@test.com',
            'phone': '(84) 99999-9999',
            'status': 'A'
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Cliente Teste'
        assert response.data['responsavel'] == self.vendor1.id
    
    def test_criar_cliente_sem_nome(self):
        """Testa que cliente sem nome falha."""
        self.client.force_authenticate(user=self.vendor1)
        
        response = self.client.post('/api/clientes/', {
            'email': 'cliente@test.com',
            'phone': '(84) 99999-9999',
            'status': 'A'
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
    
    def test_email_duplicado(self):
        """Testa que emails duplicados são rejeitados."""
        self.client.force_authenticate(user=self.vendor1)
        
        # Cria primeiro cliente
        self.client.post('/api/clientes/', {
            'name': 'Cliente 1',
            'email': 'duplicado@test.com',
            'status': 'A'
        })
        
        # Tenta criar com mesmo email
        response = self.client.post('/api/clientes/', {
            'name': 'Cliente 2',
            'email': 'duplicado@test.com',
            'status': 'A'
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    # ────────────────────────────────────────────────────
    # TESTES DE PERMISSÕES (Admin vs Vendedor)
    # ────────────────────────────────────────────────────
    
    def test_vendedor_vê_apenas_seus_clientes(self):
        """Vendedor só vê clientes que criou."""
        # Joao cria um cliente
        client_joao = Client.objects.create(
            name='Cliente de João',
            email='joao@client.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Maria cria um cliente
        client_maria = Client.objects.create(
            name='Cliente de Maria',
            email='maria@client.com',
            status='A',
            responsavel=self.vendor2
        )
        
        # João faz login e lista
        self.client.force_authenticate(user=self.vendor1)
        response = self.client.get('/api/clientes/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Cliente de João'
    
    def test_admin_vê_todos_clientes(self):
        """Admin vê TODOS os clientes de todos os vendedores."""
        # Joao cria um cliente
        Client.objects.create(
            name='Cliente de João',
            email='joao@client.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Maria cria um cliente
        Client.objects.create(
            name='Cliente de Maria',
            email='maria@client.com',
            status='A',
            responsavel=self.vendor2
        )
        
        # Admin faz login e lista
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/clientes/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_vendedor_não_edita_cliente_alheio(self):
        """Vendedor não consegue editar cliente de outro vendedor."""
        # Maria cria um cliente
        client = Client.objects.create(
            name='Cliente de Maria',
            email='maria@client.com',
            status='A',
            responsavel=self.vendor2
        )
        
        # João tenta editar
        self.client.force_authenticate(user=self.vendor1)
        response = self.client.put(f'/api/clientes/{client.id}/', {
            'name': 'Editado por João',
            'email': 'maria@client.com',
            'status': 'A'
        })
    
    # Pode retornar 403 ou 404 (ambos indicam acesso negado)
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]


    def test_admin_edita_cliente_qualquer(self):
        """Admin consegue editar cliente de qualquer vendedor."""
        # João cria um cliente
        client = Client.objects.create(
            name='Cliente de João',
            email='joao@client.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Admin edita
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f'/api/clientes/{client.id}/', {
            'name': 'Editado por Admin',
            'email': 'joao@client.com',
            'status': 'A'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Editado por Admin'

    # ────────────────────────────────────────────────────
    # TESTES DE FILTROS E BUSCA
    # ────────────────────────────────────────────────────
    
    def test_busca_por_nome_case_insensitive(self):
        """Testa busca por nome sem distinção maiúscula/minúscula."""
        self.client.force_authenticate(user=self.vendor1)
        
        # Cria clientes
        Client.objects.create(
            name='Ana Costa',
            email='ana@test.com',
            status='A',
            responsavel=self.vendor1
        )
        Client.objects.create(
            name='Bruno Silva',
            email='bruno@test.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Busca com "ana" minúsculo
        response = self.client.get('/api/clientes/?search=ana')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Ana Costa'
        
        # Busca com "ANA" maiúsculo
        response = self.client.get('/api/clientes/?search=ANA')
        assert len(response.data) == 1
    
    def test_busca_por_email(self):
        """Testa busca parcial por email."""
        self.client.force_authenticate(user=self.vendor1)
        
        Client.objects.create(
            name='Cliente Gmail',
            email='joao@gmail.com',
            status='A',
            responsavel=self.vendor1
        )
        Client.objects.create(
            name='Cliente Hotmail',
            email='maria@hotmail.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Busca por "gmail"
        response = self.client.get('/api/clientes/?search=gmail')
        assert len(response.data) == 1
        assert response.data[0]['email'] == 'joao@gmail.com'
    
    def test_busca_por_telefone(self):
        """Testa busca parcial por telefone."""
        self.client.force_authenticate(user=self.vendor1)
        
        Client.objects.create(
            name='Cliente 84',
            email='client84@test.com',
            phone='(84) 99999-9999',
            status='A',
            responsavel=self.vendor1
        )
        Client.objects.create(
            name='Cliente 11',
            email='client11@test.com',
            phone='(11) 98888-8888',
            status='A',
            responsavel=self.vendor1
        )
        
        # Busca por "84"
        response = self.client.get('/api/clientes/?search=84')
        assert len(response.data) == 1
        assert '84' in response.data[0]['phone']

    # ────────────────────────────────────────────────────
    # TESTES DE NOTAS
    # ────────────────────────────────────────────────────
    
    def test_criar_nota_em_cliente(self):
        """Testa criação de nota vinculada a cliente."""
        self.client.force_authenticate(user=self.vendor1)
        
        # Cria cliente
        client = Client.objects.create(
            name='Cliente Teste',
            email='teste@test.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Cria nota
        response = self.client.post(f'/api/clientes/{client.id}/notas/', {
            'texto': 'Cliente potencial para upgrade',
            'tipo': 'A'
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['texto'] == 'Cliente potencial para upgrade'
        assert response.data['user'] == self.vendor1.id
        assert str(response.data['client']) == str(client.id)
    def test_listar_notas_cliente(self):
        """Testa listagem de notas de um cliente."""
        self.client.force_authenticate(user=self.vendor1)
        
        # Cria cliente
        client = Client.objects.create(
            name='Cliente Teste',
            email='teste@test.com',
            status='A',
            responsavel=self.vendor1
        )
        
        # Cria 2 notas via API
        self.client.post(f'/api/clientes/{client.id}/notas/', {
            'texto': 'Nota 1',
            'tipo': 'A'
        })
        self.client.post(f'/api/clientes/{client.id}/notas/', {
            'texto': 'Nota 2',
            'tipo': 'C'
        })
        
        # Lista notas
        response = self.client.get(f'/api/clientes/{client.id}/notas/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


    def test_vendedor_não_acessa_notas_alheias(self):
        """Vendedor não vê notas de clientes de outros vendedores."""
        # Maria cria cliente
        client = Client.objects.create(
            name='Cliente de Maria',
            email='maria@test.com',
            status='A',
            responsavel=self.vendor2
        )
        
        # Maria cria uma nota via API
        self.client.force_authenticate(user=self.vendor2)
        self.client.post(f'/api/clientes/{client.id}/notas/', {
            'texto': 'Nota secreta',
            'tipo': 'A'
        })
        
        # João tenta acessar
        self.client.force_authenticate(user=self.vendor1)
        response = self.client.get(f'/api/clientes/{client.id}/notas/')
        
        # Deve retornar 404 ou vazio
        assert response.status_code == status.HTTP_404_NOT_FOUND or len(response.data) == 0