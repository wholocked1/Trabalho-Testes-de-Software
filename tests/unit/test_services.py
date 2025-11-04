import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from django.db import connection
# from rest_framework.exceptions import ValidationError as DRFValidationError #Não precisamos disto

# Importe as funções que você quer testar
from src.core.services import (
    get_professor_project_counts,
    create_project_with_associations,
    associate_assessor_to_project,
    deactivate_project_participant,
    associate_aluno_to_project,
    associate_orientador_to_project,
    link_mongo_to_project,
    save_corretor_text
)

# --- CORREÇÃO: REMOVEMOS OS IMPORTS DOS MODELOS ---
# from src.core.models import Professor, Aluno, Projeto 
# -------------------------------------------------

# Importe os serializers que o serviço usa
# from src.core.serializers import ProfessorCreateSerializer # Não precisamos disto

# NOTA: A marcação 'pytestmark' está (corretamente) removida.
# pytestmark = pytest.mark.django_db

# --- Testes para get_professor_project_counts ---

# O 'mocker' é uma fixture do pytest-mock
def test_get_professor_project_counts_success(mocker):
    """
    Testa se a função retorna a contagem correta quando o professor existe.
    Isso cobre o "caso normal".
    """
    
    # 1. ARRANGE (Arrumar)
    # --- CORREÇÃO: Usamos MagicMock em vez do modelo real ---
    fake_professor = mocker.MagicMock(id_professor=3937, nome="Prof. Teste")
    
    # "Mock" (Simular) as chamadas ao repositório
    mocker.patch(
        'src.core.services.repo.get_professor_by_id', # Onde está a função
        return_value=fake_professor                   # O que ela deve retornar
    )
    mocker.patch(
        'src.core.services.repo.get_active_orientador_count',
        return_value=5 # Retorna um número falso
    )
    mocker.patch(
        'src.core.services.repo.get_active_assessor_count',
        return_value=2 # Retorna um número falso
    )

    # 2. ACT (Agir)
    result = get_professor_project_counts(professor_id=3937)

    # 3. ASSERT (Verificar)
    assert result['orientacoes_ativas'] == 5
    assert result['assessorias_ativas'] == 2
    assert result['id_professor'] == 3937


def test_get_professor_project_counts_not_found(mocker):
    """
    Testa se a função levanta a exceção correta se o professor não existir.
    Isso cobre o "caso de erro".
    """
    
    # 1. ARRANGE (Arrumar)
    mocker.patch(
        'src.core.services.repo.get_professor_by_id',
        side_effect=ObjectDoesNotExist("Professor não encontrado")
    )

    # 2. ACT & 3. ASSERT (Verificar)
    with pytest.raises(ObjectDoesNotExist) as exc_info:
        get_professor_project_counts(professor_id=999) # ID que não existe

    assert "Professor com ID 999 não encontrado" in str(exc_info.value)


# --- Testes para create_project_with_associations ---
# @pytest.mark.django_db
def test_create_project_with_associations_existing_users(mocker):
    """
    Caso de Teste 3 (Caminho Feliz): 
    Cria um projeto com ID de professor e ID de aluno existentes.
    """
    # 1. ARRANGE (Arrumar)
    fake_data = {
        'tema': 'Novo Projeto de Teste', 'tipo': 1, 'resumo': '...', 'duracao': 12,
        'id_professor': 101,
        'id_aluno': 202
    }
    
    # --- CORREÇÃO: Usamos MagicMock em vez dos modelos reais ---
    fake_professor = mocker.MagicMock(id_professor=101, nome="Prof. Teste")
    fake_aluno = mocker.MagicMock(id_aluno=202, nome="Aluno Teste")
    fake_project = mocker.MagicMock() # Não precisa do 'spec=Projeto'
    
    # Configurar os mocks (simuladores) do repositório
    mock_get_prof = mocker.patch('src.core.services.repo.get_professor_by_id', return_value=fake_professor)
    mock_get_aluno = mocker.patch('src.core.services.repo.get_aluno_by_id', return_value=fake_aluno)
    mock_create_proj = mocker.patch('src.core.services.repo.create_project', return_value=fake_project)
    mock_create_orient = mocker.patch('src.core.services.repo.create_orientador_assoc')
    mock_create_alunoproj = mocker.patch('src.core.services.repo.create_alunoproj_assoc')

    # 2. ACT (Agir)
    result = create_project_with_associations(fake_data)

    # 3. ASSERT (Verificar)
    mock_get_prof.assert_called_once_with(101)
    mock_get_aluno.assert_called_once_with(202)
    mock_create_proj.assert_called_once_with(fake_data)
    mock_create_orient.assert_called_once_with(fake_professor, fake_project)
    mock_create_alunoproj.assert_called_once_with(fake_aluno, fake_project)
    fake_project.refresh_from_db.assert_called_once()
    assert result == fake_project

# @pytest.mark.django_db
def test_create_project_with_new_orientador(mocker):
    """
    Caso de Teste 4 (Caminho Feliz Alternativo): 
    Cria um projeto com um *novo* professor (orientador_novo).
    """
    # 1. ARRANGE
    fake_data = {
        'tema': 'Projeto com Novo Orientador', 'tipo': 2, 'resumo': '...', 'duracao': 6,
        'orientador_novo': { 'nome': 'Novo Prof.', 'email': 'novo@prof.com' },
        'id_aluno': 202
    }
    
    # --- CORREÇÃO: Usamos MagicMock em vez dos modelos reais ---
    fake_aluno = mocker.MagicMock(id_aluno=202, nome="Aluno Teste")
    fake_new_professor = mocker.MagicMock(id_professor=102, nome="Novo Prof.")
    fake_project = mocker.MagicMock()

    # Mock do Serializer (isto já estava correto, pois usa o path em string)
    mock_serializer_instance = mocker.MagicMock()
    mock_serializer_instance.is_valid.return_value = True
    mock_serializer_instance.validated_data = { 'nome': 'Novo Prof.', 'email': 'novo@prof.com' }
    
    mock_SerializerClass = mocker.patch(
        'src.core.serializers.ProfessorCreateSerializer', 
        return_value=mock_serializer_instance
    )

    # Mock dos repositórios
    mock_create_prof = mocker.patch('src.core.services.repo.create_professor', return_value=fake_new_professor)
    mock_get_aluno = mocker.patch('src.core.services.repo.get_aluno_by_id', return_value=fake_aluno)
    mock_create_proj = mocker.patch('src.core.services.repo.create_project', return_value=fake_project)
    mock_create_orient = mocker.patch('src.core.services.repo.create_orientador_assoc')
    mock_create_alunoproj = mocker.patch('src.core.services.repo.create_alunoproj_assoc')
    
    # 2. ACT
    result = create_project_with_associations(fake_data)

    # 3. ASSERT
    mock_SerializerClass.assert_called_once_with(data=fake_data['orientador_novo'])
    mock_serializer_instance.is_valid.assert_called_once_with(raise_exception=True)
    mock_create_prof.assert_called_once_with(mock_serializer_instance.validated_data)
    mock_create_orient.assert_called_once_with(fake_new_professor, fake_project)

# @pytest.mark.django_db
def test_create_project_professor_not_found(mocker):
    """
    Caso de Teste 5 (Erro): 
    Tenta criar com um ID de professor que não existe.
    """
    # 1. ARRANGE
    fake_data = {'id_professor': 999, 'id_aluno': 202} # Dados mínimos
    
    mocker.patch(
        'src.core.services.repo.get_professor_by_id',
        side_effect=ObjectDoesNotExist("Professor")
    )
    # --- CORREÇÃO: Usamos MagicMock em vez de Aluno() ---
    mocker.patch(
        'src.core.services.repo.get_aluno_by_id',
        return_value=mocker.MagicMock(id_aluno=202)
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        create_project_with_associations(fake_data)
    
    assert "Professor orientador com ID 999 não encontrado" in str(e.value)

# @pytest.mark.django_db
def test_create_project_aluno_not_found(mocker):
    """
    Caso de Teste 6 (Erro): 
    Tenta criar com um ID de aluno que não existe.
    """
    # 1. ARRANGE
    fake_data = {'id_professor': 101, 'id_aluno': 999} # Dados mínimos
    
    # --- CORREÇÃO: Usamos MagicMock em vez de Professor() ---
    fake_professor = mocker.MagicMock(id_professor=101, nome="Prof. Teste")

    mocker.patch(
        'src.core.services.repo.get_professor_by_id',
        return_value=fake_professor
    )
    mocker.patch(
        'src.core.services.repo.get_aluno_by_id',
        side_effect=ObjectDoesNotExist("Aluno")
    )
    
    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        create_project_with_associations(fake_data)
        
    assert "Aluno com ID 999 não encontrado" in str(e.value)

# --- Testes para associate_assessor_to_project ---

def test_associate_assessor_success(mocker):
    """
    Caso de Teste 7 (Caminho Feliz):
    Associa um assessor com sucesso.
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    fake_professor = mocker.MagicMock()

    # Simulamos o repositório
    mocker.patch('src.core.services.repo.get_professor_by_id', return_value=fake_professor)
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    
    # Simulamos a regra de negócio (não é o orientador)
    mocker.patch('src.core.services.repo.check_if_orientador_is_assessor', return_value=False)
    
    # Simulamos a criação da associação
    mock_create_assoc = mocker.patch('src.core.services.repo.create_assessor_assoc')

    # 2. ACT
    associate_assessor_to_project(project_id=1, assessor_id=2)

    # 3. ASSERT
    # Verificamos se a associação foi criada
    mock_create_assoc.assert_called_once_with(2, fake_project)


def test_associate_assessor_fails_if_is_orientador(mocker):
    """
    Caso de Teste 8 (Erro - Regra de Negócio):
    Falha ao tentar associar um professor que já é o orientador.
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    fake_professor = mocker.MagicMock()

    mocker.patch('src.core.services.repo.get_professor_by_id', return_value=fake_professor)
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    
    # Simulamos a regra de negócio (professor JÁ É o orientador)
    mocker.patch('src.core.services.repo.check_if_orientador_is_assessor', return_value=True)
    
    mock_create_assoc = mocker.patch('src.core.services.repo.create_assessor_assoc')

    # 2. ACT & 3. ASSERT
    # Verificamos se a exceção correta foi levantada
    with pytest.raises(ValidationError) as e:
        associate_assessor_to_project(project_id=1, assessor_id=2)
    
    # Verificamos a mensagem de erro da regra de negócio
    assert "Orientador não pode ser assessor" in str(e.value)
    
    # Verificamos que a associação NÃO foi criada
    mock_create_assoc.assert_not_called()


def test_associate_assessor_fails_if_professor_not_found(mocker):
    """
    Caso de Teste 9 (Erro):
    Falha se o ID do professor (assessor) não for encontrado.
    """
    # 1. ARRANGE
    # Simulamos o repositório falhando em encontrar o professor
    mocker.patch(
        'src.core.services.repo.get_professor_by_id', 
        side_effect=ObjectDoesNotExist("Professor")
    )
    
    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        associate_assessor_to_project(project_id=1, assessor_id=999)
        
    # Verificamos a mensagem de erro personalizada do serviço
    assert "Professor assessor com ID 999 não encontrado" in str(e.value)


def test_associate_assessor_fails_if_project_not_found(mocker):
    """
    Caso de Teste 10 (Erro):
    Falha se o ID do projeto não for encontrado.
    """
    # 1. ARRANGE
    mocker.patch('src.core.services.repo.get_professor_by_id', return_value=mocker.MagicMock())
    
    # Simulamos o repositório falhando em encontrar o projeto
    mocker.patch(
        'src.core.services.repo.get_project_by_id', 
        side_effect=ObjectDoesNotExist("Projeto")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        associate_assessor_to_project(project_id=999, assessor_id=2)
        
    # Verificamos a mensagem de erro personalizada do serviço
    assert "Projeto (ID 999) não encontrado" in str(e.value)

# --- Testes para deactivate_project_participant ---

def test_deactivate_participant_success(mocker):
    """
    Caso de Teste 11 (Caminho Feliz):
    Desativa um participante com sucesso (quando há 1 ativo).
    """
    # 1. ARRANGE
    # Criamos um "mock" para a relação (ex: AlunoProj)
    fake_relation = mocker.MagicMock()
    
    # Criamos um "mock" para o queryset (lista) retornado
    mock_queryset = mocker.MagicMock()
    mock_queryset.count.return_value = 1 # Diz que há 1 ativo
    mock_queryset.get.return_value = fake_relation # Retorna o objeto
    
    # Simulamos os repositórios
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=mocker.MagicMock())
    mocker.patch('src.core.services.repo.get_active_participant_relation', return_value=mock_queryset)
    mock_save = mocker.patch('src.core.services.repo.save_instance')

    # 2. ACT
    result = deactivate_project_participant(project_id=1, role='aluno')

    # 3. ASSERT
    # Verificamos se a contagem foi chamada
    mock_queryset.count.assert_called_once()
    # Verificamos se o objeto foi pego
    mock_queryset.get.assert_called_once()
    # Verificamos se o 'ativo' foi mudado para False
    assert fake_relation.ativo == False
    # Verificamos se o 'save' foi chamado
    mock_save.assert_called_once_with(fake_relation)
    # Verificamos a mensagem de sucesso
    assert result == 'Status do aluno atualizado para inativo.'


def test_deactivate_participant_fails_invalid_role(mocker):
    """
    Caso de Teste 12 (Erro - Validação):
    Falha se a 'role' (função) for inválida.
    """
    # 1. ARRANGE
    # Não precisamos de mocks de repositório, pois a função falha antes
    
    # 2. ACT & 3. ASSERT
    with pytest.raises(ValidationError) as e:
        deactivate_project_participant(project_id=1, role='coordenador') # Role inválida
    
    assert "Role inválido" in str(e.value)


def test_deactivate_participant_fails_project_not_found(mocker):
    """
    Caso de Teste 13 (Erro):
    Falha se o projeto não for encontrado.
    """
    # 1. ARRANGE
    mocker.patch(
        'src.core.services.repo.get_project_by_id', 
        side_effect=ObjectDoesNotExist("Projeto")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        deactivate_project_participant(project_id=999, role='aluno')
    
    assert "Projeto (ID 999) não encontrado" in str(e.value)


def test_deactivate_participant_fails_no_active_participant(mocker):
    """
    Caso de Teste 14 (Erro - Regra de Negócio):
    Falha se houver 0 participantes ativos.
    """
    # 1. ARRANGE
    mock_queryset = mocker.MagicMock()
    mock_queryset.count.return_value = 0 # Diz que há 0 ativos
    
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=mocker.MagicMock())
    mocker.patch('src.core.services.repo.get_active_participant_relation', return_value=mock_queryset)

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        deactivate_project_participant(project_id=1, role='assessor')
    
    assert "Nenhum assessor ativo encontrado" in str(e.value)


def test_deactivate_participant_fails_multiple_active_participants(mocker):
    """
    Caso de Teste 15 (Erro - Regra de Negócio):
    Falha se houver mais de 1 participante ativo.
    """
    # 1. ARRANGE
    mock_queryset = mocker.MagicMock()
    mock_queryset.count.return_value = 2 # Diz que há 2 ativos
    
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=mocker.MagicMock())
    mocker.patch('src.core.services.repo.get_active_participant_relation', return_value=mock_queryset)

    # 2. ACT & 3. ASSERT
    with pytest.raises(ValidationError) as e:
        deactivate_project_participant(project_id=1, role='orientador')
    
    assert "Múltiplos orientadors ativos" in str(e.value)

# --- Testes para associate_aluno_to_project ---

def test_associate_aluno_success(mocker):
    """
    Caso de Teste 16 (Caminho Feliz):
    Associa um aluno com sucesso.
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    fake_aluno = mocker.MagicMock()
    mock_assoc = mocker.MagicMock() # A associação criada

    # Simulamos o repositório E CAPTURAMOS OS MOCKS
    mock_get_proj = mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mock_get_aluno = mocker.patch('src.core.services.repo.get_aluno_by_id', return_value=fake_aluno)
    mock_create_assoc = mocker.patch('src.core.services.repo.create_alunoproj_assoc', return_value=mock_assoc)

    # 2. ACT
    result = associate_aluno_to_project(project_id=1, aluno_id=2)

    # 3. ASSERT
    # --- CORREÇÃO AQUI ---
    # Verificamos se as buscas foram feitas USANDO OS MOCKS CAPTURADOS
    mock_get_proj.assert_called_once_with(1)
    mock_get_aluno.assert_called_once_with(2)
    # ---------------------
    
    # Verificamos se a associação foi criada
    mock_create_assoc.assert_called_once_with(fake_aluno, fake_project)
    
    # Verificamos se o resultado é a associação
    assert result == mock_assoc


def test_associate_aluno_fails_project_not_found(mocker):
    """
    Caso de Teste 17 (Erro):
    Falha se o projeto não for encontrado.
    """
    # 1. ARRANGE
    # Simulamos o repositório falhando em encontrar o projeto
    mocker.patch(
        'src.core.services.repo.get_project_by_id', 
        side_effect=ObjectDoesNotExist("Projeto")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        associate_aluno_to_project(project_id=999, aluno_id=2)
        
    assert "Projeto (ID 999) ou Aluno (ID 2) não encontrado" in str(e.value)


def test_associate_aluno_fails_aluno_not_found(mocker):
    """
    Caso de Teste 18 (Erro):
    Falha se o aluno não for encontrado.
    """
    # 1. ARRANGE
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=mocker.MagicMock())
    
    # Simulamos o repositório falhando em encontrar o aluno
    mocker.patch(
        'src.core.services.repo.get_aluno_by_id', 
        side_effect=ObjectDoesNotExist("Aluno")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        associate_aluno_to_project(project_id=1, aluno_id=999)
        
    assert "Projeto (ID 1) ou Aluno (ID 999) não encontrado" in str(e.value)


def test_associate_aluno_fails_on_creation(mocker):
    """
    Caso de Teste 19 (Erro - Validação):
    Falha se a criação da associação levantar uma exceção (ex: ValidationError).
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    fake_aluno = mocker.MagicMock()

    mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mocker.patch('src.core.services.repo.get_aluno_by_id', return_value=fake_aluno)
    
    # Simulamos a criação da associação falhando
    mocker.patch(
        'src.core.services.repo.create_alunoproj_assoc', 
        side_effect=ValidationError("Erro de validação simulado")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ValidationError) as e:
        associate_aluno_to_project(project_id=1, aluno_id=2)
        
    assert "Erro ao associar aluno" in str(e.value)
    assert "Erro de validação simulado" in str(e.value)

# --- Testes para associate_orientador_to_project ---

def test_associate_orientador_success(mocker):
    """
    Caso de Teste 20 (Caminho Feliz):
    Associa um orientador com sucesso.
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    fake_professor = mocker.MagicMock()
    mock_assoc = mocker.MagicMock() # A associação criada

    # Simulamos o repositório E CAPTURAMOS OS MOCKS
    mock_get_proj = mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mock_get_prof = mocker.patch('src.core.services.repo.get_professor_by_id', return_value=fake_professor)
    mock_create_assoc = mocker.patch('src.core.services.repo.create_orientador_assoc', return_value=mock_assoc)

    # 2. ACT
    result = associate_orientador_to_project(project_id=1, orientador_id=2)

    # 3. ASSERT
    mock_get_proj.assert_called_once_with(1)
    mock_get_prof.assert_called_once_with(2)
    mock_create_assoc.assert_called_once_with(fake_professor, fake_project)
    assert result == mock_assoc


def test_associate_orientador_fails_project_not_found(mocker):
    """
    Caso de Teste 21 (Erro):
    Falha se o projeto não for encontrado.
    """
    # 1. ARRANGE
    mocker.patch(
        'src.core.services.repo.get_project_by_id', 
        side_effect=ObjectDoesNotExist("Projeto")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        associate_orientador_to_project(project_id=999, orientador_id=2)
        
    assert "Projeto (ID 999) não encontrado" in str(e.value)


def test_associate_orientador_fails_professor_not_found(mocker):
    """
    Caso de Teste 22 (Erro):
    Falha se o professor não for encontrado.
    """
    # 1. ARRANGE
    mocker.patch('src.core.services.repo.get_project_by_id', return_value=mocker.MagicMock())
    
    mocker.patch(
        'src.core.services.repo.get_professor_by_id', 
        side_effect=ObjectDoesNotExist("Professor")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        associate_orientador_to_project(project_id=1, orientador_id=999)
        
    assert "Professor (ID 999) não encontrado" in str(e.value)


def test_associate_orientador_fails_on_creation(mocker):
    """
    Caso de Teste 23 (Erro - Validação):
    Falha se a criação da associação levantar uma exceção (ex: ValidationError).
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    fake_professor = mocker.MagicMock()

    mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mocker.patch('src.core.services.repo.get_professor_by_id', return_value=fake_professor)
    
    mocker.patch(
        'src.core.services.repo.create_orientador_assoc', 
        side_effect=ValidationError("Erro de validação simulado")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ValidationError) as e:
        associate_orientador_to_project(project_id=1, orientador_id=2)
        
    assert "Erro ao associar orientador" in str(e.value)
    assert "Erro de validação simulado" in str(e.value)

# --- Testes para link_mongo_to_project ---

def test_link_mongo_to_project_success(mocker):
    """
    Caso de Teste 24 (Caminho Feliz):
    Associa um ID do Mongo com sucesso.
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    valid_mongo_id = "60d5ecf31234abcd1234efab" # ID válido de 24 chars

    # Simulamos o repositório
    mock_get_proj = mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mock_save = mocker.patch('src.core.services.repo.save_instance', return_value=fake_project)

    # 2. ACT
    result = link_mongo_to_project(project_id=1, mongo_id_str=valid_mongo_id)

    # 3. ASSERT
    # Verificamos se o projeto foi buscado
    mock_get_proj.assert_called_once_with(1)
    
    # Verificamos se o ID foi atribuído ao objeto do projeto
    assert fake_project.mongo_id == valid_mongo_id
    
    # Verificamos se o projeto foi salvo
    mock_save.assert_called_once_with(fake_project)
    
    # Verificamos o retorno
    assert result == fake_project


def test_link_mongo_to_project_fails_invalid_id(mocker):
    """
    Caso de Teste 25 (Erro - Validação):
    Falha se o ID do Mongo for inválido (ex: muito curto).
    """
    # 1. ARRANGE
    invalid_mongo_id = "123456789" # ID inválido (não tem 24 chars)

    # 2. ACT & 3. ASSERT
    # Verificamos se a validação da função pegou o erro
    with pytest.raises(ValidationError) as e:
        link_mongo_to_project(project_id=1, mongo_id_str=invalid_mongo_id)
        
    assert '"mongo_id" inválido' in str(e.value)


def test_link_mongo_to_project_fails_project_not_found(mocker):
    """
    Caso de Teste 26 (Erro):
    Falha se o projeto não for encontrado.
    """
    # 1. ARRANGE
    valid_mongo_id = "60d5ecf31234abcd1234efab"
    
    # Simulamos o repositório falhando em encontrar o projeto
    mocker.patch(
        'src.core.services.repo.get_project_by_id', 
        side_effect=ObjectDoesNotExist("Projeto")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        link_mongo_to_project(project_id=999, mongo_id_str=valid_mongo_id)
        
    assert "Projeto (ID 999) não encontrado" in str(e.value)

# --- Testes para save_corretor_text ---

def test_save_corretor_text_success(mocker):
    """
    Caso de Teste 27 (Caminho Feliz):
    Salva o texto do corretor com sucesso.
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    texto = "Este é um texto de exemplo."

    # Simulamos o repositório
    mock_get_proj = mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mock_save = mocker.patch('src.core.services.repo.save_instance', return_value=fake_project)

    # 2. ACT
    result = save_corretor_text(project_id=1, texto_corretor=texto)

    # 3. ASSERT
    mock_get_proj.assert_called_once_with(1)
    
    # Verificamos se o texto foi atribuído ao objeto do projeto
    assert fake_project.melhor_corretor == texto
    
    # Verificamos se o projeto foi salvo
    mock_save.assert_called_once_with(fake_project)
    assert result == fake_project


def test_save_corretor_text_success_empty_string(mocker):
    """
    Caso de Teste 28 (Caso Extremo):
    Salva com sucesso uma string vazia (que é diferente de None).
    """
    # 1. ARRANGE
    fake_project = mocker.MagicMock()
    texto = "" # String vazia (válido)

    mock_get_proj = mocker.patch('src.core.services.repo.get_project_by_id', return_value=fake_project)
    mock_save = mocker.patch('src.core.services.repo.save_instance', return_value=fake_project)

    # 2. ACT
    result = save_corretor_text(project_id=1, texto_corretor=texto)

    # 3. ASSERT
    mock_get_proj.assert_called_once_with(1)
    assert fake_project.melhor_corretor == texto # Deve salvar a string vazia
    mock_save.assert_called_once_with(fake_project)
    assert result == fake_project


def test_save_corretor_text_fails_text_is_none(mocker):
    """
    Caso de Teste 29 (Erro - Validação):
    Falha se o texto for 'None' (nulo).
    """
    # 1. ARRANGE
    texto = None # Inválido

    # 2. ACT & 3. ASSERT
    # Verificamos se a validação da função pegou o erro
    with pytest.raises(ValidationError) as e:
        save_corretor_text(project_id=1, texto_corretor=texto)
        
    assert 'O campo "texto_corretor" é obrigatório' in str(e.value)


def test_save_corretor_text_fails_project_not_found(mocker):
    """
    Caso de Teste 30 (Erro):
    Falha se o projeto não for encontrado.
    """
    # 1. ARRANGE
    texto = "Texto de teste"
    
    # Simulamos o repositório falhando em encontrar o projeto
    mocker.patch(
        'src.core.services.repo.get_project_by_id', 
        side_effect=ObjectDoesNotExist("Projeto")
    )

    # 2. ACT & 3. ASSERT
    with pytest.raises(ObjectDoesNotExist) as e:
        save_corretor_text(project_id=999, texto_corretor=texto)
        
    assert "Projeto (ID 999) não encontrado" in str(e.value)