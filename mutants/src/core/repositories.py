# core/repositories.py
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Professor, Aluno, Projeto, Departamento, ProfessorLattes, HistAluno,
    AlunoProj, Orientador, Assessor
)
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

# --- Repositório de Professor ---

def x_get_all_professors_with_dept__mutmut_orig():
    """ Retorna todos os professores, otimizando a busca pelo departamento. """
    return Professor.objects.all().select_related('departamento')

# --- Repositório de Professor ---

def x_get_all_professors_with_dept__mutmut_1():
    """ Retorna todos os professores, otimizando a busca pelo departamento. """
    return Professor.objects.all().select_related(None)

# --- Repositório de Professor ---

def x_get_all_professors_with_dept__mutmut_2():
    """ Retorna todos os professores, otimizando a busca pelo departamento. """
    return Professor.objects.all().select_related('XXdepartamentoXX')

# --- Repositório de Professor ---

def x_get_all_professors_with_dept__mutmut_3():
    """ Retorna todos os professores, otimizando a busca pelo departamento. """
    return Professor.objects.all().select_related('DEPARTAMENTO')

x_get_all_professors_with_dept__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_all_professors_with_dept__mutmut_1': x_get_all_professors_with_dept__mutmut_1, 
    'x_get_all_professors_with_dept__mutmut_2': x_get_all_professors_with_dept__mutmut_2, 
    'x_get_all_professors_with_dept__mutmut_3': x_get_all_professors_with_dept__mutmut_3
}

def get_all_professors_with_dept(*args, **kwargs):
    result = _mutmut_trampoline(x_get_all_professors_with_dept__mutmut_orig, x_get_all_professors_with_dept__mutmut_mutants, args, kwargs)
    return result 

get_all_professors_with_dept.__signature__ = _mutmut_signature(x_get_all_professors_with_dept__mutmut_orig)
x_get_all_professors_with_dept__mutmut_orig.__name__ = 'x_get_all_professors_with_dept'

def x_get_professor_by_id__mutmut_orig(professor_id):
    """ Busca um professor pelo ID. Lança Professor.DoesNotExist se não encontrar. """
    return Professor.objects.get(id_professor=professor_id)

def x_get_professor_by_id__mutmut_1(professor_id):
    """ Busca um professor pelo ID. Lança Professor.DoesNotExist se não encontrar. """
    return Professor.objects.get(id_professor=None)

x_get_professor_by_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_professor_by_id__mutmut_1': x_get_professor_by_id__mutmut_1
}

def get_professor_by_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_professor_by_id__mutmut_orig, x_get_professor_by_id__mutmut_mutants, args, kwargs)
    return result 

get_professor_by_id.__signature__ = _mutmut_signature(x_get_professor_by_id__mutmut_orig)
x_get_professor_by_id__mutmut_orig.__name__ = 'x_get_professor_by_id'

def create_professor(data):
    """ Cria um novo professor. """
    return Professor.objects.create(**data)

def get_lattes_by_professor(professor_obj):
    """ Busca o Lattes de um professor. Lança ProfessorLattes.DoesNotExist. """
    return professor_obj.professorlattes

def x_get_active_orientador_count__mutmut_orig(professor_obj):
    """ Conta orientações ativas para um professor. """
    return professor_obj.orientador_set.filter(ativo=True).count()

def x_get_active_orientador_count__mutmut_1(professor_obj):
    """ Conta orientações ativas para um professor. """
    return professor_obj.orientador_set.filter(ativo=None).count()

def x_get_active_orientador_count__mutmut_2(professor_obj):
    """ Conta orientações ativas para um professor. """
    return professor_obj.orientador_set.filter(ativo=False).count()

x_get_active_orientador_count__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_active_orientador_count__mutmut_1': x_get_active_orientador_count__mutmut_1, 
    'x_get_active_orientador_count__mutmut_2': x_get_active_orientador_count__mutmut_2
}

def get_active_orientador_count(*args, **kwargs):
    result = _mutmut_trampoline(x_get_active_orientador_count__mutmut_orig, x_get_active_orientador_count__mutmut_mutants, args, kwargs)
    return result 

get_active_orientador_count.__signature__ = _mutmut_signature(x_get_active_orientador_count__mutmut_orig)
x_get_active_orientador_count__mutmut_orig.__name__ = 'x_get_active_orientador_count'

def x_get_active_assessor_count__mutmut_orig(professor_obj):
    """ Conta assessorias ativas para um professor. """
    return professor_obj.assessor_set.filter(ativo=True).count()

def x_get_active_assessor_count__mutmut_1(professor_obj):
    """ Conta assessorias ativas para um professor. """
    return professor_obj.assessor_set.filter(ativo=None).count()

def x_get_active_assessor_count__mutmut_2(professor_obj):
    """ Conta assessorias ativas para um professor. """
    return professor_obj.assessor_set.filter(ativo=False).count()

x_get_active_assessor_count__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_active_assessor_count__mutmut_1': x_get_active_assessor_count__mutmut_1, 
    'x_get_active_assessor_count__mutmut_2': x_get_active_assessor_count__mutmut_2
}

def get_active_assessor_count(*args, **kwargs):
    result = _mutmut_trampoline(x_get_active_assessor_count__mutmut_orig, x_get_active_assessor_count__mutmut_mutants, args, kwargs)
    return result 

get_active_assessor_count.__signature__ = _mutmut_signature(x_get_active_assessor_count__mutmut_orig)
x_get_active_assessor_count__mutmut_orig.__name__ = 'x_get_active_assessor_count'

# --- Repositório de Aluno ---

def x_get_all_alunos_with_curso__mutmut_orig():
    """ Retorna todos os alunos, otimizando a busca pelo curso. """
    return Aluno.objects.all().select_related('curso')

# --- Repositório de Aluno ---

def x_get_all_alunos_with_curso__mutmut_1():
    """ Retorna todos os alunos, otimizando a busca pelo curso. """
    return Aluno.objects.all().select_related(None)

# --- Repositório de Aluno ---

def x_get_all_alunos_with_curso__mutmut_2():
    """ Retorna todos os alunos, otimizando a busca pelo curso. """
    return Aluno.objects.all().select_related('XXcursoXX')

# --- Repositório de Aluno ---

def x_get_all_alunos_with_curso__mutmut_3():
    """ Retorna todos os alunos, otimizando a busca pelo curso. """
    return Aluno.objects.all().select_related('CURSO')

x_get_all_alunos_with_curso__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_all_alunos_with_curso__mutmut_1': x_get_all_alunos_with_curso__mutmut_1, 
    'x_get_all_alunos_with_curso__mutmut_2': x_get_all_alunos_with_curso__mutmut_2, 
    'x_get_all_alunos_with_curso__mutmut_3': x_get_all_alunos_with_curso__mutmut_3
}

def get_all_alunos_with_curso(*args, **kwargs):
    result = _mutmut_trampoline(x_get_all_alunos_with_curso__mutmut_orig, x_get_all_alunos_with_curso__mutmut_mutants, args, kwargs)
    return result 

get_all_alunos_with_curso.__signature__ = _mutmut_signature(x_get_all_alunos_with_curso__mutmut_orig)
x_get_all_alunos_with_curso__mutmut_orig.__name__ = 'x_get_all_alunos_with_curso'

def x_get_aluno_by_id__mutmut_orig(aluno_id):
    """ Busca um aluno pelo ID. Lança Aluno.DoesNotExist. """
    return Aluno.objects.get(id_aluno=aluno_id)

def x_get_aluno_by_id__mutmut_1(aluno_id):
    """ Busca um aluno pelo ID. Lança Aluno.DoesNotExist. """
    return Aluno.objects.get(id_aluno=None)

x_get_aluno_by_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_aluno_by_id__mutmut_1': x_get_aluno_by_id__mutmut_1
}

def get_aluno_by_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_aluno_by_id__mutmut_orig, x_get_aluno_by_id__mutmut_mutants, args, kwargs)
    return result 

get_aluno_by_id.__signature__ = _mutmut_signature(x_get_aluno_by_id__mutmut_orig)
x_get_aluno_by_id__mutmut_orig.__name__ = 'x_get_aluno_by_id'

def x_get_historico_by_aluno_id__mutmut_orig(aluno_id):
    """ Busca o histórico de um aluno pelo ID do aluno. """
    return HistAluno.objects.filter(aluno__id_aluno=aluno_id)

def x_get_historico_by_aluno_id__mutmut_1(aluno_id):
    """ Busca o histórico de um aluno pelo ID do aluno. """
    return HistAluno.objects.filter(aluno__id_aluno=None)

x_get_historico_by_aluno_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_historico_by_aluno_id__mutmut_1': x_get_historico_by_aluno_id__mutmut_1
}

def get_historico_by_aluno_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_historico_by_aluno_id__mutmut_orig, x_get_historico_by_aluno_id__mutmut_mutants, args, kwargs)
    return result 

get_historico_by_aluno_id.__signature__ = _mutmut_signature(x_get_historico_by_aluno_id__mutmut_orig)
x_get_historico_by_aluno_id__mutmut_orig.__name__ = 'x_get_historico_by_aluno_id'

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_orig():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_1():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        None, 'orientador_set__professor', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_2():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', None, 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_3():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', None
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_4():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'orientador_set__professor', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_5():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_6():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_7():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'XXalunoproj_set__alunoXX', 'orientador_set__professor', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_8():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'ALUNOPROJ_SET__ALUNO', 'orientador_set__professor', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_9():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'XXorientador_set__professorXX', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_10():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'ORIENTADOR_SET__PROFESSOR', 'assessor_set__professor'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_11():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', 'XXassessor_set__professorXX'
    )

# --- Repositório de Projeto ---

def x_get_all_projects_prefetched__mutmut_12():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', 'ASSESSOR_SET__PROFESSOR'
    )

x_get_all_projects_prefetched__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_all_projects_prefetched__mutmut_1': x_get_all_projects_prefetched__mutmut_1, 
    'x_get_all_projects_prefetched__mutmut_2': x_get_all_projects_prefetched__mutmut_2, 
    'x_get_all_projects_prefetched__mutmut_3': x_get_all_projects_prefetched__mutmut_3, 
    'x_get_all_projects_prefetched__mutmut_4': x_get_all_projects_prefetched__mutmut_4, 
    'x_get_all_projects_prefetched__mutmut_5': x_get_all_projects_prefetched__mutmut_5, 
    'x_get_all_projects_prefetched__mutmut_6': x_get_all_projects_prefetched__mutmut_6, 
    'x_get_all_projects_prefetched__mutmut_7': x_get_all_projects_prefetched__mutmut_7, 
    'x_get_all_projects_prefetched__mutmut_8': x_get_all_projects_prefetched__mutmut_8, 
    'x_get_all_projects_prefetched__mutmut_9': x_get_all_projects_prefetched__mutmut_9, 
    'x_get_all_projects_prefetched__mutmut_10': x_get_all_projects_prefetched__mutmut_10, 
    'x_get_all_projects_prefetched__mutmut_11': x_get_all_projects_prefetched__mutmut_11, 
    'x_get_all_projects_prefetched__mutmut_12': x_get_all_projects_prefetched__mutmut_12
}

def get_all_projects_prefetched(*args, **kwargs):
    result = _mutmut_trampoline(x_get_all_projects_prefetched__mutmut_orig, x_get_all_projects_prefetched__mutmut_mutants, args, kwargs)
    return result 

get_all_projects_prefetched.__signature__ = _mutmut_signature(x_get_all_projects_prefetched__mutmut_orig)
x_get_all_projects_prefetched__mutmut_orig.__name__ = 'x_get_all_projects_prefetched'

def x_get_project_by_id__mutmut_orig(project_id):
    """ Busca um projeto pelo ID. Lança Projeto.DoesNotExist. """
    return Projeto.objects.get(id_proj=project_id)

def x_get_project_by_id__mutmut_1(project_id):
    """ Busca um projeto pelo ID. Lança Projeto.DoesNotExist. """
    return Projeto.objects.get(id_proj=None)

x_get_project_by_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_project_by_id__mutmut_1': x_get_project_by_id__mutmut_1
}

def get_project_by_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_project_by_id__mutmut_orig, x_get_project_by_id__mutmut_mutants, args, kwargs)
    return result 

get_project_by_id.__signature__ = _mutmut_signature(x_get_project_by_id__mutmut_orig)
x_get_project_by_id__mutmut_orig.__name__ = 'x_get_project_by_id'

def x_create_project__mutmut_orig(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_1(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=None,
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_2(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=None,
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_3(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=None,
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_4(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=None,
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_5(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=None,
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_6(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=None,
    )

def x_create_project__mutmut_7(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_8(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_9(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_10(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_11(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_12(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        )

def x_create_project__mutmut_13(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get(None),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_14(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('XXtemaXX'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_15(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('TEMA'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_16(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get(None),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_17(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('XXtipoXX'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_18(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('TIPO'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_19(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get(None),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_20(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('XXresumoXX'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_21(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('RESUMO'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_22(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get(None, ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_23(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', None),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_24(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get(''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_25(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_26(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('XXpalavra_chaveXX', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_27(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('PALAVRA_CHAVE', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_28(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', 'XXXX'),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_29(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get(None),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_30(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('XXduracaoXX'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_31(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('DURACAO'),
        bolsa=data.get('bolsa'),
    )

def x_create_project__mutmut_32(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get(None),
    )

def x_create_project__mutmut_33(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('XXbolsaXX'),
    )

def x_create_project__mutmut_34(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('BOLSA'),
    )

x_create_project__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_project__mutmut_1': x_create_project__mutmut_1, 
    'x_create_project__mutmut_2': x_create_project__mutmut_2, 
    'x_create_project__mutmut_3': x_create_project__mutmut_3, 
    'x_create_project__mutmut_4': x_create_project__mutmut_4, 
    'x_create_project__mutmut_5': x_create_project__mutmut_5, 
    'x_create_project__mutmut_6': x_create_project__mutmut_6, 
    'x_create_project__mutmut_7': x_create_project__mutmut_7, 
    'x_create_project__mutmut_8': x_create_project__mutmut_8, 
    'x_create_project__mutmut_9': x_create_project__mutmut_9, 
    'x_create_project__mutmut_10': x_create_project__mutmut_10, 
    'x_create_project__mutmut_11': x_create_project__mutmut_11, 
    'x_create_project__mutmut_12': x_create_project__mutmut_12, 
    'x_create_project__mutmut_13': x_create_project__mutmut_13, 
    'x_create_project__mutmut_14': x_create_project__mutmut_14, 
    'x_create_project__mutmut_15': x_create_project__mutmut_15, 
    'x_create_project__mutmut_16': x_create_project__mutmut_16, 
    'x_create_project__mutmut_17': x_create_project__mutmut_17, 
    'x_create_project__mutmut_18': x_create_project__mutmut_18, 
    'x_create_project__mutmut_19': x_create_project__mutmut_19, 
    'x_create_project__mutmut_20': x_create_project__mutmut_20, 
    'x_create_project__mutmut_21': x_create_project__mutmut_21, 
    'x_create_project__mutmut_22': x_create_project__mutmut_22, 
    'x_create_project__mutmut_23': x_create_project__mutmut_23, 
    'x_create_project__mutmut_24': x_create_project__mutmut_24, 
    'x_create_project__mutmut_25': x_create_project__mutmut_25, 
    'x_create_project__mutmut_26': x_create_project__mutmut_26, 
    'x_create_project__mutmut_27': x_create_project__mutmut_27, 
    'x_create_project__mutmut_28': x_create_project__mutmut_28, 
    'x_create_project__mutmut_29': x_create_project__mutmut_29, 
    'x_create_project__mutmut_30': x_create_project__mutmut_30, 
    'x_create_project__mutmut_31': x_create_project__mutmut_31, 
    'x_create_project__mutmut_32': x_create_project__mutmut_32, 
    'x_create_project__mutmut_33': x_create_project__mutmut_33, 
    'x_create_project__mutmut_34': x_create_project__mutmut_34
}

def create_project(*args, **kwargs):
    result = _mutmut_trampoline(x_create_project__mutmut_orig, x_create_project__mutmut_mutants, args, kwargs)
    return result 

create_project.__signature__ = _mutmut_signature(x_create_project__mutmut_orig)
x_create_project__mutmut_orig.__name__ = 'x_create_project'

def x_create_orientador_assoc__mutmut_orig(professor_obj, projeto_obj):
    """ Cria a associação de Orientador. """
    return Orientador.objects.create(professor=professor_obj, projeto=projeto_obj)

def x_create_orientador_assoc__mutmut_1(professor_obj, projeto_obj):
    """ Cria a associação de Orientador. """
    return Orientador.objects.create(professor=None, projeto=projeto_obj)

def x_create_orientador_assoc__mutmut_2(professor_obj, projeto_obj):
    """ Cria a associação de Orientador. """
    return Orientador.objects.create(professor=professor_obj, projeto=None)

def x_create_orientador_assoc__mutmut_3(professor_obj, projeto_obj):
    """ Cria a associação de Orientador. """
    return Orientador.objects.create(projeto=projeto_obj)

def x_create_orientador_assoc__mutmut_4(professor_obj, projeto_obj):
    """ Cria a associação de Orientador. """
    return Orientador.objects.create(professor=professor_obj, )

x_create_orientador_assoc__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_orientador_assoc__mutmut_1': x_create_orientador_assoc__mutmut_1, 
    'x_create_orientador_assoc__mutmut_2': x_create_orientador_assoc__mutmut_2, 
    'x_create_orientador_assoc__mutmut_3': x_create_orientador_assoc__mutmut_3, 
    'x_create_orientador_assoc__mutmut_4': x_create_orientador_assoc__mutmut_4
}

def create_orientador_assoc(*args, **kwargs):
    result = _mutmut_trampoline(x_create_orientador_assoc__mutmut_orig, x_create_orientador_assoc__mutmut_mutants, args, kwargs)
    return result 

create_orientador_assoc.__signature__ = _mutmut_signature(x_create_orientador_assoc__mutmut_orig)
x_create_orientador_assoc__mutmut_orig.__name__ = 'x_create_orientador_assoc'

def x_create_alunoproj_assoc__mutmut_orig(aluno_obj, projeto_obj):
    """ Cria a associação de AlunoProj. """
    return AlunoProj.objects.create(aluno=aluno_obj, projeto=projeto_obj)

def x_create_alunoproj_assoc__mutmut_1(aluno_obj, projeto_obj):
    """ Cria a associação de AlunoProj. """
    return AlunoProj.objects.create(aluno=None, projeto=projeto_obj)

def x_create_alunoproj_assoc__mutmut_2(aluno_obj, projeto_obj):
    """ Cria a associação de AlunoProj. """
    return AlunoProj.objects.create(aluno=aluno_obj, projeto=None)

def x_create_alunoproj_assoc__mutmut_3(aluno_obj, projeto_obj):
    """ Cria a associação de AlunoProj. """
    return AlunoProj.objects.create(projeto=projeto_obj)

def x_create_alunoproj_assoc__mutmut_4(aluno_obj, projeto_obj):
    """ Cria a associação de AlunoProj. """
    return AlunoProj.objects.create(aluno=aluno_obj, )

x_create_alunoproj_assoc__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_alunoproj_assoc__mutmut_1': x_create_alunoproj_assoc__mutmut_1, 
    'x_create_alunoproj_assoc__mutmut_2': x_create_alunoproj_assoc__mutmut_2, 
    'x_create_alunoproj_assoc__mutmut_3': x_create_alunoproj_assoc__mutmut_3, 
    'x_create_alunoproj_assoc__mutmut_4': x_create_alunoproj_assoc__mutmut_4
}

def create_alunoproj_assoc(*args, **kwargs):
    result = _mutmut_trampoline(x_create_alunoproj_assoc__mutmut_orig, x_create_alunoproj_assoc__mutmut_mutants, args, kwargs)
    return result 

create_alunoproj_assoc.__signature__ = _mutmut_signature(x_create_alunoproj_assoc__mutmut_orig)
x_create_alunoproj_assoc__mutmut_orig.__name__ = 'x_create_alunoproj_assoc'

def x_create_assessor_assoc__mutmut_orig(professor_id, projeto_obj):
    """ Cria a associação de Assessor. """
    return Assessor.objects.create(professor_id=professor_id, projeto=projeto_obj)

def x_create_assessor_assoc__mutmut_1(professor_id, projeto_obj):
    """ Cria a associação de Assessor. """
    return Assessor.objects.create(professor_id=None, projeto=projeto_obj)

def x_create_assessor_assoc__mutmut_2(professor_id, projeto_obj):
    """ Cria a associação de Assessor. """
    return Assessor.objects.create(professor_id=professor_id, projeto=None)

def x_create_assessor_assoc__mutmut_3(professor_id, projeto_obj):
    """ Cria a associação de Assessor. """
    return Assessor.objects.create(projeto=projeto_obj)

def x_create_assessor_assoc__mutmut_4(professor_id, projeto_obj):
    """ Cria a associação de Assessor. """
    return Assessor.objects.create(professor_id=professor_id, )

x_create_assessor_assoc__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_assessor_assoc__mutmut_1': x_create_assessor_assoc__mutmut_1, 
    'x_create_assessor_assoc__mutmut_2': x_create_assessor_assoc__mutmut_2, 
    'x_create_assessor_assoc__mutmut_3': x_create_assessor_assoc__mutmut_3, 
    'x_create_assessor_assoc__mutmut_4': x_create_assessor_assoc__mutmut_4
}

def create_assessor_assoc(*args, **kwargs):
    result = _mutmut_trampoline(x_create_assessor_assoc__mutmut_orig, x_create_assessor_assoc__mutmut_mutants, args, kwargs)
    return result 

create_assessor_assoc.__signature__ = _mutmut_signature(x_create_assessor_assoc__mutmut_orig)
x_create_assessor_assoc__mutmut_orig.__name__ = 'x_create_assessor_assoc'

def x_check_if_orientador_is_assessor__mutmut_orig(projeto_obj, assessor_id):
    """ Verifica se um professor já é orientador do projeto. """
    return projeto_obj.orientadores.filter(id_professor=assessor_id).exists()

def x_check_if_orientador_is_assessor__mutmut_1(projeto_obj, assessor_id):
    """ Verifica se um professor já é orientador do projeto. """
    return projeto_obj.orientadores.filter(id_professor=None).exists()

x_check_if_orientador_is_assessor__mutmut_mutants : ClassVar[MutantDict] = {
'x_check_if_orientador_is_assessor__mutmut_1': x_check_if_orientador_is_assessor__mutmut_1
}

def check_if_orientador_is_assessor(*args, **kwargs):
    result = _mutmut_trampoline(x_check_if_orientador_is_assessor__mutmut_orig, x_check_if_orientador_is_assessor__mutmut_mutants, args, kwargs)
    return result 

check_if_orientador_is_assessor.__signature__ = _mutmut_signature(x_check_if_orientador_is_assessor__mutmut_orig)
x_check_if_orientador_is_assessor__mutmut_orig.__name__ = 'x_check_if_orientador_is_assessor'

def x_get_first_orientador_departamento__mutmut_orig(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_1(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = None
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_2(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by(None).first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_3(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('XX-ativoXX').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_4(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ATIVO').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_5(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_6(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist(None)
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_7(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("XXNenhum orientador associado ao projeto.XX")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_8(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_9(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("NENHUM ORIENTADOR ASSOCIADO AO PROJETO.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_10(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_11(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist(None)
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_12(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("XXOrientador não possui departamento.XX")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_13(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("orientador não possui departamento.")
    return orientador_rel.professor.departamento

def x_get_first_orientador_departamento__mutmut_14(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("ORIENTADOR NÃO POSSUI DEPARTAMENTO.")
    return orientador_rel.professor.departamento

x_get_first_orientador_departamento__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_first_orientador_departamento__mutmut_1': x_get_first_orientador_departamento__mutmut_1, 
    'x_get_first_orientador_departamento__mutmut_2': x_get_first_orientador_departamento__mutmut_2, 
    'x_get_first_orientador_departamento__mutmut_3': x_get_first_orientador_departamento__mutmut_3, 
    'x_get_first_orientador_departamento__mutmut_4': x_get_first_orientador_departamento__mutmut_4, 
    'x_get_first_orientador_departamento__mutmut_5': x_get_first_orientador_departamento__mutmut_5, 
    'x_get_first_orientador_departamento__mutmut_6': x_get_first_orientador_departamento__mutmut_6, 
    'x_get_first_orientador_departamento__mutmut_7': x_get_first_orientador_departamento__mutmut_7, 
    'x_get_first_orientador_departamento__mutmut_8': x_get_first_orientador_departamento__mutmut_8, 
    'x_get_first_orientador_departamento__mutmut_9': x_get_first_orientador_departamento__mutmut_9, 
    'x_get_first_orientador_departamento__mutmut_10': x_get_first_orientador_departamento__mutmut_10, 
    'x_get_first_orientador_departamento__mutmut_11': x_get_first_orientador_departamento__mutmut_11, 
    'x_get_first_orientador_departamento__mutmut_12': x_get_first_orientador_departamento__mutmut_12, 
    'x_get_first_orientador_departamento__mutmut_13': x_get_first_orientador_departamento__mutmut_13, 
    'x_get_first_orientador_departamento__mutmut_14': x_get_first_orientador_departamento__mutmut_14
}

def get_first_orientador_departamento(*args, **kwargs):
    result = _mutmut_trampoline(x_get_first_orientador_departamento__mutmut_orig, x_get_first_orientador_departamento__mutmut_mutants, args, kwargs)
    return result 

get_first_orientador_departamento.__signature__ = _mutmut_signature(x_get_first_orientador_departamento__mutmut_orig)
x_get_first_orientador_departamento__mutmut_orig.__name__ = 'x_get_first_orientador_departamento'

def x_get_active_participant_relation__mutmut_orig(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_1(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = ""
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_2(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role != 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_3(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'XXalunoXX': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_4(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'ALUNO': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_5(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = None
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_6(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role != 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_7(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'XXorientadorXX': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_8(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'ORIENTADOR': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_9(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = None
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_10(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role != 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_11(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'XXassessorXX': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_12(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'ASSESSOR': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_13(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = None
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_14(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is not None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_15(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(None)
        
    return related_queryset.filter(ativo=True)

def x_get_active_participant_relation__mutmut_16(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=None)

def x_get_active_participant_relation__mutmut_17(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=False)

x_get_active_participant_relation__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_active_participant_relation__mutmut_1': x_get_active_participant_relation__mutmut_1, 
    'x_get_active_participant_relation__mutmut_2': x_get_active_participant_relation__mutmut_2, 
    'x_get_active_participant_relation__mutmut_3': x_get_active_participant_relation__mutmut_3, 
    'x_get_active_participant_relation__mutmut_4': x_get_active_participant_relation__mutmut_4, 
    'x_get_active_participant_relation__mutmut_5': x_get_active_participant_relation__mutmut_5, 
    'x_get_active_participant_relation__mutmut_6': x_get_active_participant_relation__mutmut_6, 
    'x_get_active_participant_relation__mutmut_7': x_get_active_participant_relation__mutmut_7, 
    'x_get_active_participant_relation__mutmut_8': x_get_active_participant_relation__mutmut_8, 
    'x_get_active_participant_relation__mutmut_9': x_get_active_participant_relation__mutmut_9, 
    'x_get_active_participant_relation__mutmut_10': x_get_active_participant_relation__mutmut_10, 
    'x_get_active_participant_relation__mutmut_11': x_get_active_participant_relation__mutmut_11, 
    'x_get_active_participant_relation__mutmut_12': x_get_active_participant_relation__mutmut_12, 
    'x_get_active_participant_relation__mutmut_13': x_get_active_participant_relation__mutmut_13, 
    'x_get_active_participant_relation__mutmut_14': x_get_active_participant_relation__mutmut_14, 
    'x_get_active_participant_relation__mutmut_15': x_get_active_participant_relation__mutmut_15, 
    'x_get_active_participant_relation__mutmut_16': x_get_active_participant_relation__mutmut_16, 
    'x_get_active_participant_relation__mutmut_17': x_get_active_participant_relation__mutmut_17
}

def get_active_participant_relation(*args, **kwargs):
    result = _mutmut_trampoline(x_get_active_participant_relation__mutmut_orig, x_get_active_participant_relation__mutmut_mutants, args, kwargs)
    return result 

get_active_participant_relation.__signature__ = _mutmut_signature(x_get_active_participant_relation__mutmut_orig)
x_get_active_participant_relation__mutmut_orig.__name__ = 'x_get_active_participant_relation'

def save_instance(instance):
    """ Salva qualquer instância de modelo. """
    instance.save()
    return instance

# --- Repositório de Departamento ---

def get_all_departments():
    """ Retorna todos os departamentos. """
    return Departamento.objects.all()

def x_get_lattes_keywords_by_dept_id__mutmut_orig(departamento_id):
    """ Busca keywords lattes de professores de um departamento. """
    return ProfessorLattes.objects.select_related('professor').filter(professor__departamento_id=departamento_id)

def x_get_lattes_keywords_by_dept_id__mutmut_1(departamento_id):
    """ Busca keywords lattes de professores de um departamento. """
    return ProfessorLattes.objects.select_related('professor').filter(professor__departamento_id=None)

def x_get_lattes_keywords_by_dept_id__mutmut_2(departamento_id):
    """ Busca keywords lattes de professores de um departamento. """
    return ProfessorLattes.objects.select_related(None).filter(professor__departamento_id=departamento_id)

def x_get_lattes_keywords_by_dept_id__mutmut_3(departamento_id):
    """ Busca keywords lattes de professores de um departamento. """
    return ProfessorLattes.objects.select_related('XXprofessorXX').filter(professor__departamento_id=departamento_id)

def x_get_lattes_keywords_by_dept_id__mutmut_4(departamento_id):
    """ Busca keywords lattes de professores de um departamento. """
    return ProfessorLattes.objects.select_related('PROFESSOR').filter(professor__departamento_id=departamento_id)

x_get_lattes_keywords_by_dept_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_lattes_keywords_by_dept_id__mutmut_1': x_get_lattes_keywords_by_dept_id__mutmut_1, 
    'x_get_lattes_keywords_by_dept_id__mutmut_2': x_get_lattes_keywords_by_dept_id__mutmut_2, 
    'x_get_lattes_keywords_by_dept_id__mutmut_3': x_get_lattes_keywords_by_dept_id__mutmut_3, 
    'x_get_lattes_keywords_by_dept_id__mutmut_4': x_get_lattes_keywords_by_dept_id__mutmut_4
}

def get_lattes_keywords_by_dept_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_lattes_keywords_by_dept_id__mutmut_orig, x_get_lattes_keywords_by_dept_id__mutmut_mutants, args, kwargs)
    return result 

get_lattes_keywords_by_dept_id.__signature__ = _mutmut_signature(x_get_lattes_keywords_by_dept_id__mutmut_orig)
x_get_lattes_keywords_by_dept_id__mutmut_orig.__name__ = 'x_get_lattes_keywords_by_dept_id'

# --- Outros Repositórios ---

def x_get_all_lattes_keywords__mutmut_orig():
    """ Retorna keywords de todos os professores. """
    return ProfessorLattes.objects.select_related('professor').all()

# --- Outros Repositórios ---

def x_get_all_lattes_keywords__mutmut_1():
    """ Retorna keywords de todos os professores. """
    return ProfessorLattes.objects.select_related(None).all()

# --- Outros Repositórios ---

def x_get_all_lattes_keywords__mutmut_2():
    """ Retorna keywords de todos os professores. """
    return ProfessorLattes.objects.select_related('XXprofessorXX').all()

# --- Outros Repositórios ---

def x_get_all_lattes_keywords__mutmut_3():
    """ Retorna keywords de todos os professores. """
    return ProfessorLattes.objects.select_related('PROFESSOR').all()

x_get_all_lattes_keywords__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_all_lattes_keywords__mutmut_1': x_get_all_lattes_keywords__mutmut_1, 
    'x_get_all_lattes_keywords__mutmut_2': x_get_all_lattes_keywords__mutmut_2, 
    'x_get_all_lattes_keywords__mutmut_3': x_get_all_lattes_keywords__mutmut_3
}

def get_all_lattes_keywords(*args, **kwargs):
    result = _mutmut_trampoline(x_get_all_lattes_keywords__mutmut_orig, x_get_all_lattes_keywords__mutmut_mutants, args, kwargs)
    return result 

get_all_lattes_keywords.__signature__ = _mutmut_signature(x_get_all_lattes_keywords__mutmut_orig)
x_get_all_lattes_keywords__mutmut_orig.__name__ = 'x_get_all_lattes_keywords'

def get_all_lattes():
    """ Retorna todas as entradas Lattes. """
    return ProfessorLattes.objects.all()