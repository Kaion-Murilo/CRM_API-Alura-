#!/bin/bash

# Aguarda o PostgreSQL ficar pronto
echo "Aguardando PostgreSQL..."
for i in {1..30}; do
  if python -c "import psycopg2; psycopg2.connect('postgresql://crm_user:crm_password@db:5432/crm_db')" 2>/dev/null; then
    echo "✅ PostgreSQL está pronto!"
    break
  fi
  echo "Tentativa $i/30... aguardando PostgreSQL"
  sleep 2
done

# Executa migrações
python manage.py migrate

# Cria usuários
python manage.py shell << END
from django.contrib.auth.models import User, Group

Group.objects.get_or_create(name='Administrador')
Group.objects.get_or_create(name='Vendedor')

if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    admin_group = Group.objects.get(name='Administrador')
    admin.groups.add(admin_group)
    print("✅ Admin criado: admin / admin123")

if not User.objects.filter(username='joao').exists():
    vendor = User.objects.create_user('joao', password='joao123')
    vendor_group = Group.objects.get(name='Vendedor')
    vendor.groups.add(vendor_group)
    print("✅ Vendedor criado: joao / joao123")

if not User.objects.filter(username='maria').exists():
    vendor = User.objects.create_user('maria', password='maria123')
    vendor_group = Group.objects.get(name='Vendedor')
    vendor.groups.add(vendor_group)
    print("✅ Vendedor criado: maria / maria123")

END

# Inicia o servidor
python manage.py runserver 0.0.0.0:8000