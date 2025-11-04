# tests/integration/test_integration_services.py

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# --- Desta vez, importamos os MODELOS REAIS ---
from src.core.models import (
    Professor, Aluno, Projeto, Departamento, Curso, 
    Orientador, AlunoProj
)

# --- Importamos os SERVIÇOS que vamos testar ---
from src.core.services import (
    create_project_with_associations,
    get_professor_project_counts
)

# --- ESSENCIAL ---
# Isso diz ao pytest para preparar o banco de dados de teste
# (Usando as configurações 'TEST' do seu settings.py)
pytestmark = pytest.mark.django_db


# --- Fixture: Prepara o banco de dados ---

@pytest.fixture(scope='function')
def setup_database_data():
    """
    Uma 'fixture' que cria os dados básicos no banco de dados de teste
    ANTES de cada teste nesta suíte rodar.
    """
    # 1. Limpa o banco de dados de teste (para garantir que esteja vazio)
    # (O pytest-django cuida disso, mas é bom garantir)
    Orientador.objects.all().delete()
    AlunoProj.objects.all().delete()
    Projeto.objects.all().delete()
    Professor.objects.all().delete()
    Aluno.objects.all().delete()
    Curso.objects.all().delete()
    Departamento.objects.all().delete()

    # 2. Cria dados de pré-requisito
    dept = Departamento.objects.create(id_departamento=1, nome_departamento="Eng. de Computação")
    curso = Curso.objects.create(id_curso=1, nome="Ciência da Computação", departamento=dept)
    prof = Professor.objects.create(
        id_professor=3937, 
        nome="Prof. Integração", 
        email="prof.integracao@teste.com", 
        departamento=dept
    )
    aluno = Aluno.objects.create(
        id_aluno=221240849, 
        nome="Aluno Integração", 
        email="aluno.integracao@teste.com", 
        curso=curso, 
        telefone="123456789"
    )
    
    # 3. Retorna os objetos criados para os testes usarem
    return {"prof": prof, "aluno": aluno}


# --- Testes de Integração ---

def test_integration_create_project_and_check_counts(setup_database_data):
    """
    Caso de Teste de Integração 1 (Fluxo Completo):
    1. (SETUP) Usa a fixture 'setup_database_data'.
    2. (ACT 1) Chama o SERVIÇO 'create_project_with_associations'.
    3. (ASSERT 1) Verifica se o SERVIÇO + REPOSITÓRIO criaram os dados no BD.
    4. (ACT 2) Chama o SERVIÇO 'get_professor_project_counts'.
    5. (ASSERT 2) Verifica se o SERVIÇO 2 consegue ler os dados criados pelo SERVIÇO 1.
    """
    
    # 1. ARRANGE
    # Pegamos os dados reais criados pela fixture
    prof = setup_database_data['prof']
    aluno = setup_database_data['aluno']
    
    project_data = {
        'tema': 'Projeto de Teste de Integração',
        'tipo': 1, # IC
        'resumo': 'Testando o fluxo completo service-repo-db',
        'duracao': 12,
        'id_professor': prof.id_professor,
        'id_aluno': aluno.id_aluno
    }

    # 2. ACT (Parte 1: Chamar o Serviço de Criação)
    # Sem Mocks! Estamos chamando o serviço real.
    projeto_criado = create_project_with_associations(project_data)

    # 3. ASSERT (Parte 1: Verificar o Banco de Dados)
    assert projeto_criado is not None
    assert projeto_criado.tema == "Projeto de Teste de Integração"
    
    # Verificamos se as associações (que usam o .repo) foram realmente criadas
    assert Orientador.objects.filter(projeto=projeto_criado, professor=prof, ativo=True).exists()
    assert AlunoProj.objects.filter(projeto=projeto_criado, aluno=aluno, ativo=True).exists()
    assert Projeto.objects.count() == 1

    # 4. ACT (Parte 2: Chamar o Serviço de Contagem)
    # Testamos a interação entre dois módulos de serviço
    counts = get_professor_project_counts(prof.id_professor)

    # 5. ASSERT (Parte 2: Verificar a Lógica Integrada)
    assert counts['orientacoes_ativas'] == 1
    assert counts['assessorias_ativas'] == 0