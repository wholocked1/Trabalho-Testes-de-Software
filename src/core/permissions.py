# core/permissions.py
# Arquivo não utilizado, estamos fazendo essa validação de quem pode fazer cada função pelo front-end

from rest_framework.permissions import BasePermission

def is_in_group(user, group_name):
    """
    Função auxiliar que verifica se um usuário pertence a um grupo específico.
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False

class IsOrientador(BasePermission):
    message = "Apenas Orientadores podem realizar esta ação."
    def has_permission(self, request, view):
        return is_in_group(request.user, 'Orientador')

class IsCoordenacao(BasePermission):
    message = "Apenas membros da Coordenação podem realizar esta ação."
    def has_permission(self, request, view):
        return is_in_group(request.user, 'Coordenação')

class CanCreateProject(BasePermission):
    """
    Permite a ação apenas se o usuário for do grupo Orientador OU do grupo Coordenação.
    """
    message = "Apenas Orientadores ou membros da Coordenação podem criar projetos."
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'Coordenação')  
