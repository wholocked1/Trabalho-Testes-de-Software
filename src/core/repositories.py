# core/repositories.py
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Professor, Aluno, Projeto, Departamento, ProfessorLattes, HistAluno,
    AlunoProj, Orientador, Assessor
)

# --- Repositório de Professor ---

def get_all_professors_with_dept():
    """ Retorna todos os professores, otimizando a busca pelo departamento. """
    return Professor.objects.all().select_related('departamento')

def get_professor_by_id(professor_id):
    """ Busca um professor pelo ID. Lança Professor.DoesNotExist se não encontrar. """
    return Professor.objects.get(id_professor=professor_id)

def create_professor(data):
    """ Cria um novo professor. """
    return Professor.objects.create(**data)

def get_lattes_by_professor(professor_obj):
    """ Busca o Lattes de um professor. Lança ProfessorLattes.DoesNotExist. """
    return professor_obj.professorlattes

def get_active_orientador_count(professor_obj):
    """ Conta orientações ativas para um professor. """
    return professor_obj.orientador_set.filter(ativo=True).count()

def get_active_assessor_count(professor_obj):
    """ Conta assessorias ativas para um professor. """
    return professor_obj.assessor_set.filter(ativo=True).count()

# --- Repositório de Aluno ---

def get_all_alunos_with_curso():
    """ Retorna todos os alunos, otimizando a busca pelo curso. """
    return Aluno.objects.all().select_related('curso')

def get_aluno_by_id(aluno_id):
    """ Busca um aluno pelo ID. Lança Aluno.DoesNotExist. """
    return Aluno.objects.get(id_aluno=aluno_id)

def get_historico_by_aluno_id(aluno_id):
    """ Busca o histórico de um aluno pelo ID do aluno. """
    return HistAluno.objects.filter(aluno__id_aluno=aluno_id)

# --- Repositório de Projeto ---

def get_all_projects_prefetched():
    """ Retorna todos os projetos, otimizando buscas de participantes. """
    return Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', 'assessor_set__professor'
    )

def get_project_by_id(project_id):
    """ Busca um projeto pelo ID. Lança Projeto.DoesNotExist. """
    return Projeto.objects.get(id_proj=project_id)

def create_project(data):
    """ Cria um novo projeto com os dados fornecidos. """
    return Projeto.objects.create(
        tema=data.get('tema'),
        tipo=data.get('tipo'),
        resumo=data.get('resumo'),
        palavra_chave=data.get('palavra_chave', ''),
        duracao=data.get('duracao'),
        bolsa=data.get('bolsa'),
    )

def create_orientador_assoc(professor_obj, projeto_obj):
    """ Cria a associação de Orientador. """
    return Orientador.objects.create(professor=professor_obj, projeto=projeto_obj)

def create_alunoproj_assoc(aluno_obj, projeto_obj):
    """ Cria a associação de AlunoProj. """
    return AlunoProj.objects.create(aluno=aluno_obj, projeto=projeto_obj)

def create_assessor_assoc(professor_id, projeto_obj):
    """ Cria a associação de Assessor. """
    return Assessor.objects.create(professor_id=professor_id, projeto=projeto_obj)

def check_if_orientador_is_assessor(projeto_obj, assessor_id):
    """ Verifica se um professor já é orientador do projeto. """
    return projeto_obj.orientadores.filter(id_professor=assessor_id).exists()

def get_first_orientador_departamento(projeto_obj):
    """ Busca o departamento do primeiro orientador (ativo ou não) do projeto. """
    orientador_rel = projeto_obj.orientador_set.order_by('-ativo').first()
    if not orientador_rel:
        raise ObjectDoesNotExist("Nenhum orientador associado ao projeto.")
    if not orientador_rel.professor.departamento:
        raise ObjectDoesNotExist("Orientador não possui departamento.")
    return orientador_rel.professor.departamento

def get_active_participant_relation(projeto_obj, role):
    """ Busca relações ativas de um participante (aluno, orientador, assessor). """
    related_queryset = None
    if role == 'aluno': related_queryset = projeto_obj.alunoproj_set
    elif role == 'orientador': related_queryset = projeto_obj.orientador_set
    elif role == 'assessor': related_queryset = projeto_obj.assessor_set
    
    if related_queryset is None:
        raise ValueError(f"Role '{role}' inválido.")
        
    return related_queryset.filter(ativo=True)

def save_instance(instance):
    """ Salva qualquer instância de modelo. """
    instance.save()
    return instance

# --- Repositório de Departamento ---

def get_all_departments():
    """ Retorna todos os departamentos. """
    return Departamento.objects.all()

def get_lattes_keywords_by_dept_id(departamento_id):
    """ Busca keywords lattes de professores de um departamento. """
    return ProfessorLattes.objects.select_related('professor').filter(professor__departamento_id=departamento_id)

# --- Outros Repositórios ---

def get_all_lattes_keywords():
    """ Retorna keywords de todos os professores. """
    return ProfessorLattes.objects.select_related('professor').all()

def get_all_lattes():
    """ Retorna todas as entradas Lattes. """
    return ProfessorLattes.objects.all()