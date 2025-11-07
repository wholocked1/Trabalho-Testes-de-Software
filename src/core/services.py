# src/core/services.py
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from . import repositories as repo # <-- REMOVIDO DO TOPO

# --- REVERTIDO --- (Não importamos mais o ProjetoSerializer)
# 

# --- Serviço de Professor ---

def get_professor_project_counts(professor_id):
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

# --- Serviço de Projeto ---

# @transaction.atomic
def create_project_with_associations(data):
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

def associate_aluno_to_project(project_id, aluno_id):
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

def associate_assessor_to_project(project_id, assessor_id):
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

def associate_orientador_to_project(project_id, orientador_id):
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

def link_mongo_to_project(project_id, mongo_id_str):
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

def save_corretor_text(project_id, texto_corretor):
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

def deactivate_project_participant(project_id, role):
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