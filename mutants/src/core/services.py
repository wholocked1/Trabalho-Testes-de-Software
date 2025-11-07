# src/core/services.py
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
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
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_orig(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_1(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = None
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_2(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(None)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_3(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = None
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_4(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(None)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_5(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = None
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_6(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(None)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_7(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'XXid_professorXX': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_8(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'ID_PROFESSOR': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_9(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'XXnome_professorXX': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_10(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'NOME_PROFESSOR': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_11(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'XXorientacoes_ativasXX': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_12(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'ORIENTACOES_ATIVAS': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_13(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'XXassessorias_ativasXX': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_14(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'ASSESSORIAS_ATIVAS': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Professor com ID {professor_id} não encontrado.")
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def x_get_professor_project_counts__mutmut_15(professor_id):
    """ 
    Regra de negócio: Calcular contagens de projetos ativos 
    para um professor.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        professor = repo.get_professor_by_id(professor_id)
        contagem_orientador = repo.get_active_orientador_count(professor)
        contagem_assessor = repo.get_active_assessor_count(professor)
        
        return {
            'id_professor': professor.id_professor,
            'nome_professor': professor.nome,
            'orientacoes_ativas': contagem_orientador,
            'assessorias_ativas': contagem_assessor
        }
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(None)

x_get_professor_project_counts__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_professor_project_counts__mutmut_1': x_get_professor_project_counts__mutmut_1, 
    'x_get_professor_project_counts__mutmut_2': x_get_professor_project_counts__mutmut_2, 
    'x_get_professor_project_counts__mutmut_3': x_get_professor_project_counts__mutmut_3, 
    'x_get_professor_project_counts__mutmut_4': x_get_professor_project_counts__mutmut_4, 
    'x_get_professor_project_counts__mutmut_5': x_get_professor_project_counts__mutmut_5, 
    'x_get_professor_project_counts__mutmut_6': x_get_professor_project_counts__mutmut_6, 
    'x_get_professor_project_counts__mutmut_7': x_get_professor_project_counts__mutmut_7, 
    'x_get_professor_project_counts__mutmut_8': x_get_professor_project_counts__mutmut_8, 
    'x_get_professor_project_counts__mutmut_9': x_get_professor_project_counts__mutmut_9, 
    'x_get_professor_project_counts__mutmut_10': x_get_professor_project_counts__mutmut_10, 
    'x_get_professor_project_counts__mutmut_11': x_get_professor_project_counts__mutmut_11, 
    'x_get_professor_project_counts__mutmut_12': x_get_professor_project_counts__mutmut_12, 
    'x_get_professor_project_counts__mutmut_13': x_get_professor_project_counts__mutmut_13, 
    'x_get_professor_project_counts__mutmut_14': x_get_professor_project_counts__mutmut_14, 
    'x_get_professor_project_counts__mutmut_15': x_get_professor_project_counts__mutmut_15
}

def get_professor_project_counts(*args, **kwargs):
    result = _mutmut_trampoline(x_get_professor_project_counts__mutmut_orig, x_get_professor_project_counts__mutmut_mutants, args, kwargs)
    return result 

get_professor_project_counts.__signature__ = _mutmut_signature(x_get_professor_project_counts__mutmut_orig)
x_get_professor_project_counts__mutmut_orig.__name__ = 'x_get_professor_project_counts'

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_orig(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_1(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = None
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_2(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get(None)
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_3(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('XXid_professorXX')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_4(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('ID_PROFESSOR')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_5(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = None
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_6(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get(None)
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_7(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('XXorientador_novoXX')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_8(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('ORIENTADOR_NOVO')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_9(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = None

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_10(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get(None)

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_11(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('XXid_alunoXX')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_12(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('ID_ALUNO')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_13(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = ""
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_14(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = ""

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_15(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = None
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_16(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=None)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_17(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=None)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_18(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=False)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_19(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = None
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_20(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(None)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_21(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = None

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_22(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(None)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_23(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = None

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_24(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(None)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_25(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = None
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_26(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop(None, None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_27(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop(None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_28(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', )
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_29(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('XXid_professorXX', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_30(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('ID_PROFESSOR', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_31(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop(None, None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_32(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop(None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_33(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', )
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_34(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('XXid_alunoXX', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_35(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('ID_ALUNO', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_36(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop(None, None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_37(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop(None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_38(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', )
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_39(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('XXorientador_novoXX', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_40(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('ORIENTADOR_NOVO', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_41(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = None
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_42(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(None)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_43(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(None, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_44(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, None)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_45(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_46(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, )
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_47(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(None, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_48(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, None)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_49(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_50(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, )

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_51(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'XXProfessorXX' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_52(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_53(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'PROFESSOR' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_54(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' not in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_55(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(None):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_56(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(None)
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_57(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'XXAlunoXX' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_58(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'aluno' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_59(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'ALUNO' in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_60(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' not in str(e):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_61(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(None):
             raise ObjectDoesNotExist(f'Aluno com ID {aluno_id_input} não encontrado.')
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

# --- Serviço de Projeto ---

# @transaction.atomic
def x_create_project_with_associations__mutmut_62(data):
    """ 
    Regra de negócio complexa: Criar um projeto...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    
    # --- REVERTIDO ---
    # ...
    # -----------------

    orientador_id_input = data.get('id_professor')
    orientador_novo_dados = data.get('orientador_novo')
    aluno_id_input = data.get('id_aluno')

    orientador_obj = None
    aluno_obj = None

    try:
        from .serializers import ProfessorCreateSerializer
        if orientador_novo_dados:
            prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
            prof_serializer.is_valid(raise_exception=True)
            orientador_obj = repo.create_professor(prof_serializer.validated_data)
        elif orientador_id_input:
            orientador_obj = repo.get_professor_by_id(orientador_id_input)

        if aluno_id_input:
            aluno_obj = repo.get_aluno_by_id(aluno_id_input)

        # --- CORREÇÃO DO "SUSPEITO 1" AQUI ---
        # Filtra o dicionário 'data' para conter apenas 
        # os campos que o modelo 'Projeto' realmente possui.
        
        # Crie uma cópia para não modificar o 'data' original
        projeto_data = data.copy()
        
        # Remova as chaves que NÃO pertencem ao modelo Projeto
        projeto_data.pop('id_professor', None)
        projeto_data.pop('id_aluno', None)
        projeto_data.pop('orientador_novo', None)
        # Adicione outros .pop() se houver mais campos que não são do Projeto

        # Agora criamos o projeto apenas com os dados relevantes
        projeto = repo.create_project(projeto_data)
        # --- FIM DA CORREÇÃO ---

        if orientador_obj:
            repo.create_orientador_assoc(orientador_obj, projeto)
        if aluno_obj:
            repo.create_alunoproj_assoc(aluno_obj, projeto)

        projeto.refresh_from_db()
        return projeto

    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f'Professor orientador com ID {orientador_id_input} não encontrado.')
        if 'Aluno' in str(e):
             raise ObjectDoesNotExist(None)
        raise e
    except (IntegrityError, ValidationError) as e:
        raise e

x_create_project_with_associations__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_project_with_associations__mutmut_1': x_create_project_with_associations__mutmut_1, 
    'x_create_project_with_associations__mutmut_2': x_create_project_with_associations__mutmut_2, 
    'x_create_project_with_associations__mutmut_3': x_create_project_with_associations__mutmut_3, 
    'x_create_project_with_associations__mutmut_4': x_create_project_with_associations__mutmut_4, 
    'x_create_project_with_associations__mutmut_5': x_create_project_with_associations__mutmut_5, 
    'x_create_project_with_associations__mutmut_6': x_create_project_with_associations__mutmut_6, 
    'x_create_project_with_associations__mutmut_7': x_create_project_with_associations__mutmut_7, 
    'x_create_project_with_associations__mutmut_8': x_create_project_with_associations__mutmut_8, 
    'x_create_project_with_associations__mutmut_9': x_create_project_with_associations__mutmut_9, 
    'x_create_project_with_associations__mutmut_10': x_create_project_with_associations__mutmut_10, 
    'x_create_project_with_associations__mutmut_11': x_create_project_with_associations__mutmut_11, 
    'x_create_project_with_associations__mutmut_12': x_create_project_with_associations__mutmut_12, 
    'x_create_project_with_associations__mutmut_13': x_create_project_with_associations__mutmut_13, 
    'x_create_project_with_associations__mutmut_14': x_create_project_with_associations__mutmut_14, 
    'x_create_project_with_associations__mutmut_15': x_create_project_with_associations__mutmut_15, 
    'x_create_project_with_associations__mutmut_16': x_create_project_with_associations__mutmut_16, 
    'x_create_project_with_associations__mutmut_17': x_create_project_with_associations__mutmut_17, 
    'x_create_project_with_associations__mutmut_18': x_create_project_with_associations__mutmut_18, 
    'x_create_project_with_associations__mutmut_19': x_create_project_with_associations__mutmut_19, 
    'x_create_project_with_associations__mutmut_20': x_create_project_with_associations__mutmut_20, 
    'x_create_project_with_associations__mutmut_21': x_create_project_with_associations__mutmut_21, 
    'x_create_project_with_associations__mutmut_22': x_create_project_with_associations__mutmut_22, 
    'x_create_project_with_associations__mutmut_23': x_create_project_with_associations__mutmut_23, 
    'x_create_project_with_associations__mutmut_24': x_create_project_with_associations__mutmut_24, 
    'x_create_project_with_associations__mutmut_25': x_create_project_with_associations__mutmut_25, 
    'x_create_project_with_associations__mutmut_26': x_create_project_with_associations__mutmut_26, 
    'x_create_project_with_associations__mutmut_27': x_create_project_with_associations__mutmut_27, 
    'x_create_project_with_associations__mutmut_28': x_create_project_with_associations__mutmut_28, 
    'x_create_project_with_associations__mutmut_29': x_create_project_with_associations__mutmut_29, 
    'x_create_project_with_associations__mutmut_30': x_create_project_with_associations__mutmut_30, 
    'x_create_project_with_associations__mutmut_31': x_create_project_with_associations__mutmut_31, 
    'x_create_project_with_associations__mutmut_32': x_create_project_with_associations__mutmut_32, 
    'x_create_project_with_associations__mutmut_33': x_create_project_with_associations__mutmut_33, 
    'x_create_project_with_associations__mutmut_34': x_create_project_with_associations__mutmut_34, 
    'x_create_project_with_associations__mutmut_35': x_create_project_with_associations__mutmut_35, 
    'x_create_project_with_associations__mutmut_36': x_create_project_with_associations__mutmut_36, 
    'x_create_project_with_associations__mutmut_37': x_create_project_with_associations__mutmut_37, 
    'x_create_project_with_associations__mutmut_38': x_create_project_with_associations__mutmut_38, 
    'x_create_project_with_associations__mutmut_39': x_create_project_with_associations__mutmut_39, 
    'x_create_project_with_associations__mutmut_40': x_create_project_with_associations__mutmut_40, 
    'x_create_project_with_associations__mutmut_41': x_create_project_with_associations__mutmut_41, 
    'x_create_project_with_associations__mutmut_42': x_create_project_with_associations__mutmut_42, 
    'x_create_project_with_associations__mutmut_43': x_create_project_with_associations__mutmut_43, 
    'x_create_project_with_associations__mutmut_44': x_create_project_with_associations__mutmut_44, 
    'x_create_project_with_associations__mutmut_45': x_create_project_with_associations__mutmut_45, 
    'x_create_project_with_associations__mutmut_46': x_create_project_with_associations__mutmut_46, 
    'x_create_project_with_associations__mutmut_47': x_create_project_with_associations__mutmut_47, 
    'x_create_project_with_associations__mutmut_48': x_create_project_with_associations__mutmut_48, 
    'x_create_project_with_associations__mutmut_49': x_create_project_with_associations__mutmut_49, 
    'x_create_project_with_associations__mutmut_50': x_create_project_with_associations__mutmut_50, 
    'x_create_project_with_associations__mutmut_51': x_create_project_with_associations__mutmut_51, 
    'x_create_project_with_associations__mutmut_52': x_create_project_with_associations__mutmut_52, 
    'x_create_project_with_associations__mutmut_53': x_create_project_with_associations__mutmut_53, 
    'x_create_project_with_associations__mutmut_54': x_create_project_with_associations__mutmut_54, 
    'x_create_project_with_associations__mutmut_55': x_create_project_with_associations__mutmut_55, 
    'x_create_project_with_associations__mutmut_56': x_create_project_with_associations__mutmut_56, 
    'x_create_project_with_associations__mutmut_57': x_create_project_with_associations__mutmut_57, 
    'x_create_project_with_associations__mutmut_58': x_create_project_with_associations__mutmut_58, 
    'x_create_project_with_associations__mutmut_59': x_create_project_with_associations__mutmut_59, 
    'x_create_project_with_associations__mutmut_60': x_create_project_with_associations__mutmut_60, 
    'x_create_project_with_associations__mutmut_61': x_create_project_with_associations__mutmut_61, 
    'x_create_project_with_associations__mutmut_62': x_create_project_with_associations__mutmut_62
}

def create_project_with_associations(*args, **kwargs):
    result = _mutmut_trampoline(x_create_project_with_associations__mutmut_orig, x_create_project_with_associations__mutmut_mutants, args, kwargs)
    return result 

create_project_with_associations.__signature__ = _mutmut_signature(x_create_project_with_associations__mutmut_orig)
x_create_project_with_associations__mutmut_orig.__name__ = 'x_create_project_with_associations'

def x_associate_aluno_to_project__mutmut_orig(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_1(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = None
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_2(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(None)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_3(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = None
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_4(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(None)
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_5(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(None, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_6(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, None)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_7(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_8(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, )
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_9(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(None)
    except Exception as e:
        raise ValidationError(f"Erro ao associar aluno: {e}")

def x_associate_aluno_to_project__mutmut_10(project_id, aluno_id):
    """ Associa um aluno a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        aluno = repo.get_aluno_by_id(aluno_id)
        return repo.create_alunoproj_assoc(aluno, projeto)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) ou Aluno (ID {aluno_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(None)

x_associate_aluno_to_project__mutmut_mutants : ClassVar[MutantDict] = {
'x_associate_aluno_to_project__mutmut_1': x_associate_aluno_to_project__mutmut_1, 
    'x_associate_aluno_to_project__mutmut_2': x_associate_aluno_to_project__mutmut_2, 
    'x_associate_aluno_to_project__mutmut_3': x_associate_aluno_to_project__mutmut_3, 
    'x_associate_aluno_to_project__mutmut_4': x_associate_aluno_to_project__mutmut_4, 
    'x_associate_aluno_to_project__mutmut_5': x_associate_aluno_to_project__mutmut_5, 
    'x_associate_aluno_to_project__mutmut_6': x_associate_aluno_to_project__mutmut_6, 
    'x_associate_aluno_to_project__mutmut_7': x_associate_aluno_to_project__mutmut_7, 
    'x_associate_aluno_to_project__mutmut_8': x_associate_aluno_to_project__mutmut_8, 
    'x_associate_aluno_to_project__mutmut_9': x_associate_aluno_to_project__mutmut_9, 
    'x_associate_aluno_to_project__mutmut_10': x_associate_aluno_to_project__mutmut_10
}

def associate_aluno_to_project(*args, **kwargs):
    result = _mutmut_trampoline(x_associate_aluno_to_project__mutmut_orig, x_associate_aluno_to_project__mutmut_mutants, args, kwargs)
    return result 

associate_aluno_to_project.__signature__ = _mutmut_signature(x_associate_aluno_to_project__mutmut_orig)
x_associate_aluno_to_project__mutmut_orig.__name__ = 'x_associate_aluno_to_project'

def x_associate_assessor_to_project__mutmut_orig(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_1(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(None) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_2(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = None
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_3(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(None)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_4(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(None, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_5(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, None):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_6(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_7(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, ):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_8(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError(None)
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_9(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("XXOrientador não pode ser assessor.XX")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_10(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_11(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("ORIENTADOR NÃO PODE SER ASSESSOR.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_12(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(None, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_13(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, None)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_14(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_15(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, )
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_16(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'XXProfessorXX' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_17(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_18(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'PROFESSOR' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_19(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' not in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_20(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(None):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_21(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(None)
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_22(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(None)
    except Exception as e:
        raise ValidationError(f"Erro ao associar assessor: {e}")

def x_associate_assessor_to_project__mutmut_23(project_id, assessor_id):
    """ 
    Regra de negócio: Associa um assessor, 
    verificando se ele já não é o orientador.
    """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        # Garante que o professor assessor existe antes de tentar associar
        repo.get_professor_by_id(assessor_id) # Se não existir, falha aqui
        
        projeto = repo.get_project_by_id(project_id)
        
        # Regra de negócio: Orientador não pode ser assessor
        if repo.check_if_orientador_is_assessor(projeto, assessor_id):
            raise ValidationError("Orientador não pode ser assessor.")
            
        return repo.create_assessor_assoc(assessor_id, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
             raise ObjectDoesNotExist(f"Professor assessor com ID {assessor_id} não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(None)

x_associate_assessor_to_project__mutmut_mutants : ClassVar[MutantDict] = {
'x_associate_assessor_to_project__mutmut_1': x_associate_assessor_to_project__mutmut_1, 
    'x_associate_assessor_to_project__mutmut_2': x_associate_assessor_to_project__mutmut_2, 
    'x_associate_assessor_to_project__mutmut_3': x_associate_assessor_to_project__mutmut_3, 
    'x_associate_assessor_to_project__mutmut_4': x_associate_assessor_to_project__mutmut_4, 
    'x_associate_assessor_to_project__mutmut_5': x_associate_assessor_to_project__mutmut_5, 
    'x_associate_assessor_to_project__mutmut_6': x_associate_assessor_to_project__mutmut_6, 
    'x_associate_assessor_to_project__mutmut_7': x_associate_assessor_to_project__mutmut_7, 
    'x_associate_assessor_to_project__mutmut_8': x_associate_assessor_to_project__mutmut_8, 
    'x_associate_assessor_to_project__mutmut_9': x_associate_assessor_to_project__mutmut_9, 
    'x_associate_assessor_to_project__mutmut_10': x_associate_assessor_to_project__mutmut_10, 
    'x_associate_assessor_to_project__mutmut_11': x_associate_assessor_to_project__mutmut_11, 
    'x_associate_assessor_to_project__mutmut_12': x_associate_assessor_to_project__mutmut_12, 
    'x_associate_assessor_to_project__mutmut_13': x_associate_assessor_to_project__mutmut_13, 
    'x_associate_assessor_to_project__mutmut_14': x_associate_assessor_to_project__mutmut_14, 
    'x_associate_assessor_to_project__mutmut_15': x_associate_assessor_to_project__mutmut_15, 
    'x_associate_assessor_to_project__mutmut_16': x_associate_assessor_to_project__mutmut_16, 
    'x_associate_assessor_to_project__mutmut_17': x_associate_assessor_to_project__mutmut_17, 
    'x_associate_assessor_to_project__mutmut_18': x_associate_assessor_to_project__mutmut_18, 
    'x_associate_assessor_to_project__mutmut_19': x_associate_assessor_to_project__mutmut_19, 
    'x_associate_assessor_to_project__mutmut_20': x_associate_assessor_to_project__mutmut_20, 
    'x_associate_assessor_to_project__mutmut_21': x_associate_assessor_to_project__mutmut_21, 
    'x_associate_assessor_to_project__mutmut_22': x_associate_assessor_to_project__mutmut_22, 
    'x_associate_assessor_to_project__mutmut_23': x_associate_assessor_to_project__mutmut_23
}

def associate_assessor_to_project(*args, **kwargs):
    result = _mutmut_trampoline(x_associate_assessor_to_project__mutmut_orig, x_associate_assessor_to_project__mutmut_mutants, args, kwargs)
    return result 

associate_assessor_to_project.__signature__ = _mutmut_signature(x_associate_assessor_to_project__mutmut_orig)
x_associate_assessor_to_project__mutmut_orig.__name__ = 'x_associate_assessor_to_project'

def x_associate_orientador_to_project__mutmut_orig(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_1(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = None
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_2(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(None)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_3(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = None
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_4(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(None)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_5(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(None, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_6(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, None)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_7(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_8(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, )
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_9(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'XXProfessorXX' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_10(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_11(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'PROFESSOR' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_12(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' not in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_13(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(None):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_14(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(None)
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_15(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(None)
    except Exception as e:
        raise ValidationError(f"Erro ao associar orientador: {e}")

def x_associate_orientador_to_project__mutmut_16(project_id, orientador_id):
    """ Associa um orientador a um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    try:
        projeto = repo.get_project_by_id(project_id)
        professor = repo.get_professor_by_id(orientador_id)
        return repo.create_orientador_assoc(professor, projeto)
    except ObjectDoesNotExist as e:
        if 'Professor' in str(e):
            raise ObjectDoesNotExist(f"Professor (ID {orientador_id}) não encontrado.")
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
    except Exception as e:
        raise ValidationError(None)

x_associate_orientador_to_project__mutmut_mutants : ClassVar[MutantDict] = {
'x_associate_orientador_to_project__mutmut_1': x_associate_orientador_to_project__mutmut_1, 
    'x_associate_orientador_to_project__mutmut_2': x_associate_orientador_to_project__mutmut_2, 
    'x_associate_orientador_to_project__mutmut_3': x_associate_orientador_to_project__mutmut_3, 
    'x_associate_orientador_to_project__mutmut_4': x_associate_orientador_to_project__mutmut_4, 
    'x_associate_orientador_to_project__mutmut_5': x_associate_orientador_to_project__mutmut_5, 
    'x_associate_orientador_to_project__mutmut_6': x_associate_orientador_to_project__mutmut_6, 
    'x_associate_orientador_to_project__mutmut_7': x_associate_orientador_to_project__mutmut_7, 
    'x_associate_orientador_to_project__mutmut_8': x_associate_orientador_to_project__mutmut_8, 
    'x_associate_orientador_to_project__mutmut_9': x_associate_orientador_to_project__mutmut_9, 
    'x_associate_orientador_to_project__mutmut_10': x_associate_orientador_to_project__mutmut_10, 
    'x_associate_orientador_to_project__mutmut_11': x_associate_orientador_to_project__mutmut_11, 
    'x_associate_orientador_to_project__mutmut_12': x_associate_orientador_to_project__mutmut_12, 
    'x_associate_orientador_to_project__mutmut_13': x_associate_orientador_to_project__mutmut_13, 
    'x_associate_orientador_to_project__mutmut_14': x_associate_orientador_to_project__mutmut_14, 
    'x_associate_orientador_to_project__mutmut_15': x_associate_orientador_to_project__mutmut_15, 
    'x_associate_orientador_to_project__mutmut_16': x_associate_orientador_to_project__mutmut_16
}

def associate_orientador_to_project(*args, **kwargs):
    result = _mutmut_trampoline(x_associate_orientador_to_project__mutmut_orig, x_associate_orientador_to_project__mutmut_mutants, args, kwargs)
    return result 

associate_orientador_to_project.__signature__ = _mutmut_signature(x_associate_orientador_to_project__mutmut_orig)
x_associate_orientador_to_project__mutmut_orig.__name__ = 'x_associate_orientador_to_project'

def x_link_mongo_to_project__mutmut_orig(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_1(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str and len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_2(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_3(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) == 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_4(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 25:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_5(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError(None)
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_6(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('XX"mongo_id" inválido. Deve ter 24 caracteres.XX')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_7(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_8(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"MONGO_ID" INVÁLIDO. DEVE TER 24 CARACTERES.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_9(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = None
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_10(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(None)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_11(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = None
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_12(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(None)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_link_mongo_to_project__mutmut_13(project_id, mongo_id_str):
    """ Valida e salva um Mongo ID em um projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if not mongo_id_str or len(mongo_id_str) != 24:
        raise ValidationError('"mongo_id" inválido. Deve ter 24 caracteres.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.mongo_id = mongo_id_str
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(None)

x_link_mongo_to_project__mutmut_mutants : ClassVar[MutantDict] = {
'x_link_mongo_to_project__mutmut_1': x_link_mongo_to_project__mutmut_1, 
    'x_link_mongo_to_project__mutmut_2': x_link_mongo_to_project__mutmut_2, 
    'x_link_mongo_to_project__mutmut_3': x_link_mongo_to_project__mutmut_3, 
    'x_link_mongo_to_project__mutmut_4': x_link_mongo_to_project__mutmut_4, 
    'x_link_mongo_to_project__mutmut_5': x_link_mongo_to_project__mutmut_5, 
    'x_link_mongo_to_project__mutmut_6': x_link_mongo_to_project__mutmut_6, 
    'x_link_mongo_to_project__mutmut_7': x_link_mongo_to_project__mutmut_7, 
    'x_link_mongo_to_project__mutmut_8': x_link_mongo_to_project__mutmut_8, 
    'x_link_mongo_to_project__mutmut_9': x_link_mongo_to_project__mutmut_9, 
    'x_link_mongo_to_project__mutmut_10': x_link_mongo_to_project__mutmut_10, 
    'x_link_mongo_to_project__mutmut_11': x_link_mongo_to_project__mutmut_11, 
    'x_link_mongo_to_project__mutmut_12': x_link_mongo_to_project__mutmut_12, 
    'x_link_mongo_to_project__mutmut_13': x_link_mongo_to_project__mutmut_13
}

def link_mongo_to_project(*args, **kwargs):
    result = _mutmut_trampoline(x_link_mongo_to_project__mutmut_orig, x_link_mongo_to_project__mutmut_mutants, args, kwargs)
    return result 

link_mongo_to_project.__signature__ = _mutmut_signature(x_link_mongo_to_project__mutmut_orig)
x_link_mongo_to_project__mutmut_orig.__name__ = 'x_link_mongo_to_project'

def x_save_corretor_text__mutmut_orig(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_1(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is not None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_2(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError(None)
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_3(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('XXO campo "texto_corretor" é obrigatório.XX')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_4(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('o campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_5(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O CAMPO "TEXTO_CORRETOR" É OBRIGATÓRIO.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_6(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = None
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_7(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(None)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_8(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = None
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_9(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(None)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")

def x_save_corretor_text__mutmut_10(project_id, texto_corretor):
    """ Salva o texto do 'melhor_corretor' no projeto. """
    from . import repositories as repo # <-- IMPORT AQUI
    if texto_corretor is None:
        raise ValidationError('O campo "texto_corretor" é obrigatório.')
        
    try:
        projeto = repo.get_project_by_id(project_id)
        projeto.melhor_corretor = texto_corretor
        return repo.save_instance(projeto)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(None)

x_save_corretor_text__mutmut_mutants : ClassVar[MutantDict] = {
'x_save_corretor_text__mutmut_1': x_save_corretor_text__mutmut_1, 
    'x_save_corretor_text__mutmut_2': x_save_corretor_text__mutmut_2, 
    'x_save_corretor_text__mutmut_3': x_save_corretor_text__mutmut_3, 
    'x_save_corretor_text__mutmut_4': x_save_corretor_text__mutmut_4, 
    'x_save_corretor_text__mutmut_5': x_save_corretor_text__mutmut_5, 
    'x_save_corretor_text__mutmut_6': x_save_corretor_text__mutmut_6, 
    'x_save_corretor_text__mutmut_7': x_save_corretor_text__mutmut_7, 
    'x_save_corretor_text__mutmut_8': x_save_corretor_text__mutmut_8, 
    'x_save_corretor_text__mutmut_9': x_save_corretor_text__mutmut_9, 
    'x_save_corretor_text__mutmut_10': x_save_corretor_text__mutmut_10
}

def save_corretor_text(*args, **kwargs):
    result = _mutmut_trampoline(x_save_corretor_text__mutmut_orig, x_save_corretor_text__mutmut_mutants, args, kwargs)
    return result 

save_corretor_text.__signature__ = _mutmut_signature(x_save_corretor_text__mutmut_orig)
x_save_corretor_text__mutmut_orig.__name__ = 'x_save_corretor_text'

def x_deactivate_project_participant__mutmut_orig(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_1(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role and role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_2(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_3(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_4(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['XXalunoXX', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_5(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['ALUNO', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_6(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'XXorientadorXX', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_7(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'ORIENTADOR', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_8(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'XXassessorXX']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_9(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'ASSESSOR']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_10(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError(None)

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_11(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('XXRole inválido. Deve ser "aluno", "orientador" ou "assessor".XX')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_12(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('role inválido. deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_13(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('ROLE INVÁLIDO. DEVE SER "ALUNO", "ORIENTADOR" OU "ASSESSOR".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_14(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = None
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_15(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(None)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_16(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = None
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_17(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(None, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_18(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, None)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_19(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_20(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, )
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_21(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = None
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_22(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem != 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_23(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 1:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_24(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(None)
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_25(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem >= 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_26(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 2:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_27(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(None)
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_28(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = None
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_29(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = None
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_30(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = True
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_31(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(None)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_32(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'XXProjetoXX' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_33(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'projeto' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_34(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'PROJETO' in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_35(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' not in str(e):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_36(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(None):
             raise ObjectDoesNotExist(f"Projeto (ID {project_id}) não encontrado.")
        raise e

def x_deactivate_project_participant__mutmut_37(project_id, role):
    """ 
    Regra de negócio complexa: Desativa um participante...
    """
    from . import repositories as repo # <-- IMPORT AQUI
    if not role or role not in ['aluno', 'orientador', 'assessor']:
        raise ValidationError('Role inválido. Deve ser "aluno", "orientador" ou "assessor".')

    try:
        projeto = repo.get_project_by_id(project_id)
        rel_ativos = repo.get_active_participant_relation(projeto, role)
        contagem = rel_ativos.count()
        
        if contagem == 0:
            raise ObjectDoesNotExist(f'Nenhum {role} ativo encontrado para este projeto.')
        elif contagem > 1:
            raise ValidationError(f'Múltiplos {role}s ativos. Desativação automática não permitida.')
        else:
            rel = rel_ativos.get()
            rel.ativo = False
            repo.save_instance(rel)
            return f'Status do {role} atualizado para inativo.'
            
    except ObjectDoesNotExist as e:
        if 'Projeto' in str(e):
             raise ObjectDoesNotExist(None)
        raise e

x_deactivate_project_participant__mutmut_mutants : ClassVar[MutantDict] = {
'x_deactivate_project_participant__mutmut_1': x_deactivate_project_participant__mutmut_1, 
    'x_deactivate_project_participant__mutmut_2': x_deactivate_project_participant__mutmut_2, 
    'x_deactivate_project_participant__mutmut_3': x_deactivate_project_participant__mutmut_3, 
    'x_deactivate_project_participant__mutmut_4': x_deactivate_project_participant__mutmut_4, 
    'x_deactivate_project_participant__mutmut_5': x_deactivate_project_participant__mutmut_5, 
    'x_deactivate_project_participant__mutmut_6': x_deactivate_project_participant__mutmut_6, 
    'x_deactivate_project_participant__mutmut_7': x_deactivate_project_participant__mutmut_7, 
    'x_deactivate_project_participant__mutmut_8': x_deactivate_project_participant__mutmut_8, 
    'x_deactivate_project_participant__mutmut_9': x_deactivate_project_participant__mutmut_9, 
    'x_deactivate_project_participant__mutmut_10': x_deactivate_project_participant__mutmut_10, 
    'x_deactivate_project_participant__mutmut_11': x_deactivate_project_participant__mutmut_11, 
    'x_deactivate_project_participant__mutmut_12': x_deactivate_project_participant__mutmut_12, 
    'x_deactivate_project_participant__mutmut_13': x_deactivate_project_participant__mutmut_13, 
    'x_deactivate_project_participant__mutmut_14': x_deactivate_project_participant__mutmut_14, 
    'x_deactivate_project_participant__mutmut_15': x_deactivate_project_participant__mutmut_15, 
    'x_deactivate_project_participant__mutmut_16': x_deactivate_project_participant__mutmut_16, 
    'x_deactivate_project_participant__mutmut_17': x_deactivate_project_participant__mutmut_17, 
    'x_deactivate_project_participant__mutmut_18': x_deactivate_project_participant__mutmut_18, 
    'x_deactivate_project_participant__mutmut_19': x_deactivate_project_participant__mutmut_19, 
    'x_deactivate_project_participant__mutmut_20': x_deactivate_project_participant__mutmut_20, 
    'x_deactivate_project_participant__mutmut_21': x_deactivate_project_participant__mutmut_21, 
    'x_deactivate_project_participant__mutmut_22': x_deactivate_project_participant__mutmut_22, 
    'x_deactivate_project_participant__mutmut_23': x_deactivate_project_participant__mutmut_23, 
    'x_deactivate_project_participant__mutmut_24': x_deactivate_project_participant__mutmut_24, 
    'x_deactivate_project_participant__mutmut_25': x_deactivate_project_participant__mutmut_25, 
    'x_deactivate_project_participant__mutmut_26': x_deactivate_project_participant__mutmut_26, 
    'x_deactivate_project_participant__mutmut_27': x_deactivate_project_participant__mutmut_27, 
    'x_deactivate_project_participant__mutmut_28': x_deactivate_project_participant__mutmut_28, 
    'x_deactivate_project_participant__mutmut_29': x_deactivate_project_participant__mutmut_29, 
    'x_deactivate_project_participant__mutmut_30': x_deactivate_project_participant__mutmut_30, 
    'x_deactivate_project_participant__mutmut_31': x_deactivate_project_participant__mutmut_31, 
    'x_deactivate_project_participant__mutmut_32': x_deactivate_project_participant__mutmut_32, 
    'x_deactivate_project_participant__mutmut_33': x_deactivate_project_participant__mutmut_33, 
    'x_deactivate_project_participant__mutmut_34': x_deactivate_project_participant__mutmut_34, 
    'x_deactivate_project_participant__mutmut_35': x_deactivate_project_participant__mutmut_35, 
    'x_deactivate_project_participant__mutmut_36': x_deactivate_project_participant__mutmut_36, 
    'x_deactivate_project_participant__mutmut_37': x_deactivate_project_participant__mutmut_37
}

def deactivate_project_participant(*args, **kwargs):
    result = _mutmut_trampoline(x_deactivate_project_participant__mutmut_orig, x_deactivate_project_participant__mutmut_mutants, args, kwargs)
    return result 

deactivate_project_participant.__signature__ = _mutmut_signature(x_deactivate_project_participant__mutmut_orig)
x_deactivate_project_participant__mutmut_orig.__name__ = 'x_deactivate_project_participant'