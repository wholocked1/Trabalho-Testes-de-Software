import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from django.db import connection
# from rest_framework.exceptions import ValidationError as DRFValidationError #Não precisamos disto

# Importe as funções que você quer testar
from src.core.services import (
    get_professor_project_counts,
    create_project_with_associations
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