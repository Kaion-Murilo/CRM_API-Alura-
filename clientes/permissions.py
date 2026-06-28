from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permissão customizada: permite acesso se:
    - Usuário é administrador (superuser), OU
    - Usuário é o responsável pelo cliente (owner)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin pode tudo
        if request.user.is_superuser:
            return True
        
        # Vendedor só acessa seus próprios
        return obj.responsavel == request.user