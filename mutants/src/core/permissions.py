# core/permissions.py
# Arquivo não utilizado, estamos fazendo essa validação de quem pode fazer cada função pelo front-end

from rest_framework.permissions import BasePermission
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

def x_is_in_group__mutmut_orig(user, group_name):
    """
    Função auxiliar que verifica se um usuário pertence a um grupo específico.
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False

def x_is_in_group__mutmut_1(user, group_name):
    """
    Função auxiliar que verifica se um usuário pertence a um grupo específico.
    """
    if user.is_authenticated:
        return user.groups.filter(name=None).exists()
    return False

def x_is_in_group__mutmut_2(user, group_name):
    """
    Função auxiliar que verifica se um usuário pertence a um grupo específico.
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return True

x_is_in_group__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_in_group__mutmut_1': x_is_in_group__mutmut_1, 
    'x_is_in_group__mutmut_2': x_is_in_group__mutmut_2
}

def is_in_group(*args, **kwargs):
    result = _mutmut_trampoline(x_is_in_group__mutmut_orig, x_is_in_group__mutmut_mutants, args, kwargs)
    return result 

is_in_group.__signature__ = _mutmut_signature(x_is_in_group__mutmut_orig)
x_is_in_group__mutmut_orig.__name__ = 'x_is_in_group'

class IsOrientador(BasePermission):
    message = "Apenas Orientadores podem realizar esta ação."
    def xǁIsOrientadorǁhas_permission__mutmut_orig(self, request, view):
        return is_in_group(request.user, 'Orientador')
    def xǁIsOrientadorǁhas_permission__mutmut_1(self, request, view):
        return is_in_group(None, 'Orientador')
    def xǁIsOrientadorǁhas_permission__mutmut_2(self, request, view):
        return is_in_group(request.user, None)
    def xǁIsOrientadorǁhas_permission__mutmut_3(self, request, view):
        return is_in_group('Orientador')
    def xǁIsOrientadorǁhas_permission__mutmut_4(self, request, view):
        return is_in_group(request.user, )
    def xǁIsOrientadorǁhas_permission__mutmut_5(self, request, view):
        return is_in_group(request.user, 'XXOrientadorXX')
    def xǁIsOrientadorǁhas_permission__mutmut_6(self, request, view):
        return is_in_group(request.user, 'orientador')
    def xǁIsOrientadorǁhas_permission__mutmut_7(self, request, view):
        return is_in_group(request.user, 'ORIENTADOR')
    
    xǁIsOrientadorǁhas_permission__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIsOrientadorǁhas_permission__mutmut_1': xǁIsOrientadorǁhas_permission__mutmut_1, 
        'xǁIsOrientadorǁhas_permission__mutmut_2': xǁIsOrientadorǁhas_permission__mutmut_2, 
        'xǁIsOrientadorǁhas_permission__mutmut_3': xǁIsOrientadorǁhas_permission__mutmut_3, 
        'xǁIsOrientadorǁhas_permission__mutmut_4': xǁIsOrientadorǁhas_permission__mutmut_4, 
        'xǁIsOrientadorǁhas_permission__mutmut_5': xǁIsOrientadorǁhas_permission__mutmut_5, 
        'xǁIsOrientadorǁhas_permission__mutmut_6': xǁIsOrientadorǁhas_permission__mutmut_6, 
        'xǁIsOrientadorǁhas_permission__mutmut_7': xǁIsOrientadorǁhas_permission__mutmut_7
    }
    
    def has_permission(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIsOrientadorǁhas_permission__mutmut_orig"), object.__getattribute__(self, "xǁIsOrientadorǁhas_permission__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has_permission.__signature__ = _mutmut_signature(xǁIsOrientadorǁhas_permission__mutmut_orig)
    xǁIsOrientadorǁhas_permission__mutmut_orig.__name__ = 'xǁIsOrientadorǁhas_permission'

class IsCoordenacao(BasePermission):
    message = "Apenas membros da Coordenação podem realizar esta ação."
    def xǁIsCoordenacaoǁhas_permission__mutmut_orig(self, request, view):
        return is_in_group(request.user, 'Coordenação')
    def xǁIsCoordenacaoǁhas_permission__mutmut_1(self, request, view):
        return is_in_group(None, 'Coordenação')
    def xǁIsCoordenacaoǁhas_permission__mutmut_2(self, request, view):
        return is_in_group(request.user, None)
    def xǁIsCoordenacaoǁhas_permission__mutmut_3(self, request, view):
        return is_in_group('Coordenação')
    def xǁIsCoordenacaoǁhas_permission__mutmut_4(self, request, view):
        return is_in_group(request.user, )
    def xǁIsCoordenacaoǁhas_permission__mutmut_5(self, request, view):
        return is_in_group(request.user, 'XXCoordenaçãoXX')
    def xǁIsCoordenacaoǁhas_permission__mutmut_6(self, request, view):
        return is_in_group(request.user, 'coordenação')
    def xǁIsCoordenacaoǁhas_permission__mutmut_7(self, request, view):
        return is_in_group(request.user, 'COORDENAÇÃO')
    
    xǁIsCoordenacaoǁhas_permission__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁIsCoordenacaoǁhas_permission__mutmut_1': xǁIsCoordenacaoǁhas_permission__mutmut_1, 
        'xǁIsCoordenacaoǁhas_permission__mutmut_2': xǁIsCoordenacaoǁhas_permission__mutmut_2, 
        'xǁIsCoordenacaoǁhas_permission__mutmut_3': xǁIsCoordenacaoǁhas_permission__mutmut_3, 
        'xǁIsCoordenacaoǁhas_permission__mutmut_4': xǁIsCoordenacaoǁhas_permission__mutmut_4, 
        'xǁIsCoordenacaoǁhas_permission__mutmut_5': xǁIsCoordenacaoǁhas_permission__mutmut_5, 
        'xǁIsCoordenacaoǁhas_permission__mutmut_6': xǁIsCoordenacaoǁhas_permission__mutmut_6, 
        'xǁIsCoordenacaoǁhas_permission__mutmut_7': xǁIsCoordenacaoǁhas_permission__mutmut_7
    }
    
    def has_permission(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁIsCoordenacaoǁhas_permission__mutmut_orig"), object.__getattribute__(self, "xǁIsCoordenacaoǁhas_permission__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has_permission.__signature__ = _mutmut_signature(xǁIsCoordenacaoǁhas_permission__mutmut_orig)
    xǁIsCoordenacaoǁhas_permission__mutmut_orig.__name__ = 'xǁIsCoordenacaoǁhas_permission'

class CanCreateProject(BasePermission):
    """
    Permite a ação apenas se o usuário for do grupo Orientador OU do grupo Coordenação.
    """
    message = "Apenas Orientadores ou membros da Coordenação podem criar projetos."
    def xǁCanCreateProjectǁhas_permission__mutmut_orig(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_1(self, request, view):
        if (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_2(self, request, view):
        if not (request.user or request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_3(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return True
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_4(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') and is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_5(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(None, 'Orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_6(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, None) or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_7(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group('Orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_8(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, ) or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_9(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'XXOrientadorXX') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_10(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'orientador') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_11(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'ORIENTADOR') or is_in_group(request.user, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_12(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(None, 'Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_13(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, None)  
    def xǁCanCreateProjectǁhas_permission__mutmut_14(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group('Coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_15(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, )  
    def xǁCanCreateProjectǁhas_permission__mutmut_16(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'XXCoordenaçãoXX')  
    def xǁCanCreateProjectǁhas_permission__mutmut_17(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'coordenação')  
    def xǁCanCreateProjectǁhas_permission__mutmut_18(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return is_in_group(request.user, 'Orientador') or is_in_group(request.user, 'COORDENAÇÃO')  
    
    xǁCanCreateProjectǁhas_permission__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCanCreateProjectǁhas_permission__mutmut_1': xǁCanCreateProjectǁhas_permission__mutmut_1, 
        'xǁCanCreateProjectǁhas_permission__mutmut_2': xǁCanCreateProjectǁhas_permission__mutmut_2, 
        'xǁCanCreateProjectǁhas_permission__mutmut_3': xǁCanCreateProjectǁhas_permission__mutmut_3, 
        'xǁCanCreateProjectǁhas_permission__mutmut_4': xǁCanCreateProjectǁhas_permission__mutmut_4, 
        'xǁCanCreateProjectǁhas_permission__mutmut_5': xǁCanCreateProjectǁhas_permission__mutmut_5, 
        'xǁCanCreateProjectǁhas_permission__mutmut_6': xǁCanCreateProjectǁhas_permission__mutmut_6, 
        'xǁCanCreateProjectǁhas_permission__mutmut_7': xǁCanCreateProjectǁhas_permission__mutmut_7, 
        'xǁCanCreateProjectǁhas_permission__mutmut_8': xǁCanCreateProjectǁhas_permission__mutmut_8, 
        'xǁCanCreateProjectǁhas_permission__mutmut_9': xǁCanCreateProjectǁhas_permission__mutmut_9, 
        'xǁCanCreateProjectǁhas_permission__mutmut_10': xǁCanCreateProjectǁhas_permission__mutmut_10, 
        'xǁCanCreateProjectǁhas_permission__mutmut_11': xǁCanCreateProjectǁhas_permission__mutmut_11, 
        'xǁCanCreateProjectǁhas_permission__mutmut_12': xǁCanCreateProjectǁhas_permission__mutmut_12, 
        'xǁCanCreateProjectǁhas_permission__mutmut_13': xǁCanCreateProjectǁhas_permission__mutmut_13, 
        'xǁCanCreateProjectǁhas_permission__mutmut_14': xǁCanCreateProjectǁhas_permission__mutmut_14, 
        'xǁCanCreateProjectǁhas_permission__mutmut_15': xǁCanCreateProjectǁhas_permission__mutmut_15, 
        'xǁCanCreateProjectǁhas_permission__mutmut_16': xǁCanCreateProjectǁhas_permission__mutmut_16, 
        'xǁCanCreateProjectǁhas_permission__mutmut_17': xǁCanCreateProjectǁhas_permission__mutmut_17, 
        'xǁCanCreateProjectǁhas_permission__mutmut_18': xǁCanCreateProjectǁhas_permission__mutmut_18
    }
    
    def has_permission(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCanCreateProjectǁhas_permission__mutmut_orig"), object.__getattribute__(self, "xǁCanCreateProjectǁhas_permission__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has_permission.__signature__ = _mutmut_signature(xǁCanCreateProjectǁhas_permission__mutmut_orig)
    xǁCanCreateProjectǁhas_permission__mutmut_orig.__name__ = 'xǁCanCreateProjectǁhas_permission'
