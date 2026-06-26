from django.contrib import admin
from clientes.models import Client

class Clientes(admin.ModelAdmin):
    list_display = ('id','name','email','phone','status','created_at','updated_at')
    list_display_links = ('id','name',)
    list_per_page = 20
    search_fields = ('name',)
        
admin.site.register(Client,Clientes)