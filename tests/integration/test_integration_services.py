# tests/integration/test_integration_services.py

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# --- MODELOS E SERVIÇOS NÃO SÃO IMPORTADOS AQUI NO TOPO ---
# (Isso corrige o RuntimeError durante a coleta)

# --- ESSENCIAL ---
# Isso diz ao pytest para preparar o banco de dados de teste
pytestmark = pytest.mark.django_db


# --- Fixture: Prepara o banco de dados ---

@pytest.fixture(scope='function')
def setup_database_data():
    """
    Uma 'fixture' que cria os dados básicos no banco de dados de teste
    ANTES de cada teste nesta suíte rodar.
    """
    
    # --- IMPORTAMOS OS MODELOS AQUI DENTRO ---
    from src.core.models import (
        Professor, Aluno, Projeto, Departamento, Curso, 
        Orientador, AlunoProj
    )
    # ------------------------------------------

    # 1. Limpa o banco de dados de teste
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
    ...
    """
    
    # --- IMPORTAMOS MODELOS E SERVIÇOS AQUI DENTRO ---
    from src.core.models import Orientador, AlunoProj, Projeto
    from src.core.services import (
        create_project_with_associations,
        get_professor_project_counts
    )
    # -------------------------------------------------
    
    # 1. ARRANGE
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
    projeto_criado = create_project_with_associations(project_data)

    # 3. ASSERT (Parte 1: Verificar o Banco de Dados)
    assert projeto_criado is not None
    assert projeto_criado.tema == "Projeto de Teste de Integração"
    
    assert Orientador.objects.filter(projeto=projeto_criado, professor=prof, ativo=True).exists()
    assert AlunoProj.objects.filter(projeto=projeto_criado, aluno=aluno, ativo=True).exists()
    assert Projeto.objects.count() == 1

    # 4. ACT (Parte 2: Chamar o Serviço de Contagem)
    counts = get_professor_project_counts(prof.id_professor)

    # 5. ASSERT (Parte 2: Verificar a Lógica Integrada)
    assert counts['orientacoes_ativas'] == 1
    assert counts['assessorias_ativas'] == 0

def test_integration_get_all_professors(setup_database_data):
    """
    Teste de Integração 2: Verifica a função get_all_professors_with_dept.
    
    Este teste cumpre o requisito de Teste de Integração (1 de 10) e
    cobre a linha 12 do repositories.py.
    """
    # --- Imports ---
    # Importamos as funções que queremos testar (do repositório)
    from src.core.repositories import get_all_professors_with_dept
    # Importamos o Model para criar dados de teste
    from src.core.models import Professor

    # 1. ARRANGE
    # A fixture 'setup_database_data' já limpou o banco e criou
    # o "Prof. Integração". Vamos pegá-lo.
    prof1 = setup_database_data['prof']
    
    # Vamos criar um segundo professor para garantir que a lista funciona
    Professor.objects.create(
        id_professor=3938, 
        nome="Prof. Segundo", 
        email="prof.segundo@teste.com", 
        departamento=prof1.departamento # Usando o mesmo depto da fixture
    )

    # 2. ACT
    # Chamamos a função do repositório diretamente (sem mock)
    all_professors = get_all_professors_with_dept()

    # 3. ASSERT
    # Verificamos se a consulta ao banco de dados real retornou 2 professores
    assert all_professors.count() == 2
    
    # Opcional: checar se os nomes corretos estão lá
    professor_names = {prof.nome for prof in all_professors}
    assert "Prof. Integração" in professor_names
    assert "Prof. Segundo" in professor_names

def test_integration_get_all_alunos(setup_database_data):
    """
    Teste de Integração 3: Verifica a função get_all_alunos_with_curso.
    
    Este teste cumpre o requisito de Teste de Integração (2 de 10) e
    cobre a linha 38 do repositories.py.
    """
    # --- Imports ---
    from src.core.repositories import get_all_alunos_with_curso
    from src.core.models import Aluno

    # 1. ARRANGE
    # A fixture 'setup_database_data' já limpou o banco e criou
    # o "Aluno Integração".
    aluno1 = setup_database_data['aluno']
    
    # Vamos criar um segundo aluno
    Aluno.objects.create(
        id_aluno=221240850, 
        nome="Aluno Segundo", 
        email="aluno.segundo@teste.com", 
        curso=aluno1.curso, # Usando o mesmo curso da fixture
        telefone="987654321"
    )

    # 2. ACT
    # Chamamos a função do repositório diretamente
    all_alunos = get_all_alunos_with_curso()

    # 3. ASSERT
    assert all_alunos.count() == 2
    
    aluno_names = {aluno.nome for aluno in all_alunos}
    assert "Aluno Integração" in aluno_names
    assert "Aluno Segundo" in aluno_names

def test_integration_get_all_projects(setup_database_data):
    """
    Teste de Integração 4: Verifica a função get_all_projects_prefetched.
    
    Este teste cumpre o requisito de Teste de Integração (3 de 10) e
    cobre a linha 52 do repositories.py.
    """
    # --- Imports ---
    from src.core.repositories import get_all_projects_prefetched
    from src.core.models import Projeto

    # 1. ARRANGE
    # A fixture nos dá o prof e o aluno, mas não cria projetos.
    # Vamos criar dois projetos.
    prof = setup_database_data['prof']
    aluno = setup_database_data['aluno']
    
    Projeto.objects.create(
        tema="Projeto de Teste 1",
        tipo=Projeto.TipoPesquisa.INICIACAO_CIENTIFICA,
        resumo="Resumo 1",
        duracao=12
    )
    Projeto.objects.create(
        tema="Projeto de Teste 2",
        tipo=Projeto.TipoPesquisa.TCC,
        resumo="Resumo 2",
        duracao=6
    )

    # 2. ACT
    # Chamamos a função do repositório diretamente
    all_projects = get_all_projects_prefetched()

    # 3. ASSERT
    # Verificamos se o banco de dados real retornou os 2 projetos
    assert all_projects.count() == 2
    
    project_temas = {proj.tema for proj in all_projects}
    assert "Projeto de Teste 1" in project_temas
    assert "Projeto de Teste 2" in project_temas

def test_integration_get_project_by_id(setup_database_data):
    """
    Teste de Integração 5: Verifica a função get_project_by_id.
    
    Este teste cumpre o requisito de Teste de Integração (4 de 10) e
    cobre a linha 58 (repositories.py) e linhas 110-112 (models.py).
    """
    # --- Imports ---
    from src.core.repositories import get_project_by_id
    from src.core.models import Projeto

    # 1. ARRANGE
    # Cria um projeto novo especificamente para este teste
    projeto_criado = Projeto.objects.create(
        tema="Projeto Específico para ID",
        tipo=Projeto.TipoPesquisa.TCC,
        resumo="Resumo...",
        duracao=6
    )
    
    # Pega o ID dele
    id_alvo = projeto_criado.id_proj

    # 2. ACT
    # Chamamos a função do repositório diretamente
    projeto_encontrado = get_project_by_id(id_alvo)
    
    # Isso força a cobertura do __str__ (linhas 110-112 do models.py)
    str(projeto_encontrado) 

    # 3. ASSERT
    assert projeto_encontrado is not None
    assert projeto_encontrado.id_proj == id_alvo
    assert projeto_encontrado.tema == "Projeto Específico para ID"

def test_integration_get_aluno_historico(setup_database_data):
    """
    Teste de Integração 6: Verifica a função get_historico_by_aluno_id.
    
    Este teste cumpre o requisito de Teste de Integração (5 de 10) e
    cobre a linha 46 (repositories.py) e linhas 182-185 (models.py).
    """
    # --- Imports ---
    from src.core.repositories import get_historico_by_aluno_id
    from src.core.models import HistAluno, Departamento

    # 1. ARRANGE
    # Pegamos o aluno e o departamento da fixture
    aluno = setup_database_data['aluno']
    
    # O departamento do professor/curso na fixture é Eng. de Computação
    # Precisamos dele para criar o histórico
    departamento = Departamento.objects.get(nome_departamento="Eng. de Computação")

    # Criamos uma entrada de histórico para esse aluno
    hist_entry = HistAluno.objects.create(
        aluno=aluno,
        departamento=departamento,
        cod_disciplina="CC8550",
        aprovado=True
    )

    # 2. ACT
    # Chamamos a função do repositório diretamente
    historico_aluno = get_historico_by_aluno_id(aluno.id_aluno)
    
    # Força a cobertura do __str__ (linhas 182-185 do models.py)
    str(hist_entry)

    # 3. ASSERT
    assert historico_aluno.count() == 1
    assert historico_aluno.first().cod_disciplina == "CC8550"
    assert historico_aluno.first().aprovado == True

def test_integration_get_professor_lattes(setup_database_data):
    """
    Teste de Integração 7: Verifica a função get_lattes_by_professor.
    
    Este teste cumpre o requisito de Teste de Integração (6 de 10) e
    cobre a linha 20 (repositories.py) e 20-21 (serializers.py).
    """
    # --- Imports ---
    from src.core.repositories import get_lattes_by_professor
    from src.core.models import ProfessorLattes
    from src.core.serializers import ProfessorSerializer

    # 1. ARRANGE
    # Pegamos o professor da fixture
    professor = setup_database_data['prof']
    
    # Criamos um Lattes para ele
    lattes_obj = ProfessorLattes.objects.create(
        professor=professor,
        cod_lattes="123456789",
        link="http://lattes.cnpq.br/123456789"
    )

    # 2. ACT
    # Chamamos a função do repositório diretamente
    lattes_encontrado = get_lattes_by_professor(professor)
    
    # Vamos também testar o serializer para cobrir as linhas 20-21
    # O "get_lattes_link" é chamado pelo serializer
    serializer = ProfessorSerializer(instance=professor)
    serializer_data = serializer.data

    # 3. ASSERT
    assert lattes_encontrado is not None
    assert lattes_encontrado.cod_lattes == "123456789"
    
    # Verifica se o serializer cobriu as linhas
    assert serializer_data['lattes_link'] == "http://lattes.cnpq.br/123456789"

def test_integration_associate_assessor(setup_database_data):
    """
    Teste de Integração 8: Verifica o serviço associate_assessor_to_project.
    
    Este teste cumpre o requisito de Teste de Integração (7 de 10) e
    cobre as linhas 81 e 85 do repositories.py.
    """
    # --- Imports ---
    from src.core.services import associate_assessor_to_project
    from src.core.models import Projeto, Professor, Assessor

    # 1. ARRANGE
    # A fixture nos dá um professor (prof) e um aluno.
    # Precisamos de um PROJETO e um segundo PROFESSOR (para ser o assessor).
    
    prof_orientador = setup_database_data['prof']
    
    # Cria um segundo professor (o futuro assessor)
    prof_assessor = Professor.objects.create(
        id_professor=3939, 
        nome="Prof. Assessor", 
        email="prof.assessor@teste.com", 
        departamento=prof_orientador.departamento
    )
    
    # Cria um projeto
    projeto = Projeto.objects.create(
        tema="Projeto para Testar Associação",
        tipo=Projeto.TipoPesquisa.TCC,
        resumo="Resumo...",
        duracao=12
    )
    # Adiciona o orientador (necessário para a regra de negócio)
    projeto.orientadores.add(prof_orientador)

    # 2. ACT
    # Chamamos a função do SERVIÇO diretamente
    associate_assessor_to_project(
        project_id=projeto.id_proj, 
        assessor_id=prof_assessor.id_professor
    )

    # 3. ASSERT
    # Verificamos no banco se a associação foi criada
    assert Assessor.objects.filter(
        projeto=projeto, 
        professor=prof_assessor
    ).exists()
    
    # Verifica se o projeto realmente tem 1 assessor
    projeto.refresh_from_db()
    assert projeto.assessores.count() == 1
    assert projeto.assessores.first().nome == "Prof. Assessor"

def test_integration_deactivate_participant(setup_database_data):
    """
    Teste de Integração 9: Verifica o serviço deactivate_project_participant.
    
    Este teste cumpre o requisito de Teste de Integração (8 de 10) e
    cobre as linhas 98-106 e 110-111 do repositories.py.
    """
    # --- Imports ---
    from src.core.services import deactivate_project_participant
    from src.core.models import Projeto, AlunoProj

    # 1. ARRANGE
    # Precisamos de um projeto com um aluno ativo
    aluno = setup_database_data['aluno']
    
    projeto = Projeto.objects.create(
        tema="Projeto para Desativar Aluno",
        tipo=Projeto.TipoPesquisa.TCC,
        resumo="Resumo...",
        duracao=12
    )
    
    # Cria a associação de aluno ATIVA
    assoc = AlunoProj.objects.create(aluno=aluno, projeto=projeto, ativo=True)

    # Garante que o estado inicial está correto
    assert assoc.ativo is True

    # 2. ACT
    # Chamamos a função do SERVIÇO diretamente
    deactivate_project_participant(
        project_id=projeto.id_proj, 
        role='aluno'
    )

    # 3. ASSERT
    # Verificamos no banco se a associação foi desativada
    assoc.refresh_from_db()
    assert assoc.ativo is False

def test_integration_fail_associate_second_aluno_to_ic(setup_database_data):
    """
    Teste de Integração 10: Verifica a regra de negócio (IC só pode ter 1 aluno).
    
    Este teste cumpre o requisito de Teste de Integração (9 de 10) e
    cobre as linhas 132-134 (models.py) e 93-95 (services.py).
    """
    # --- Imports ---
    import pytest
    from django.core.exceptions import ValidationError
    from src.core.services import associate_aluno_to_project
    from src.core.models import Projeto, Aluno

    # 1. ARRANGE
    # Pega o primeiro aluno da fixture
    aluno1 = setup_database_data['aluno']
    
    # Cria um segundo aluno
    aluno2 = Aluno.objects.create(
        id_aluno=221240851, 
        nome="Aluno Extra", 
        email="aluno.extra@teste.com", 
        curso=aluno1.curso,
        telefone="111111"
    )
    
    # Cria um projeto de INICIAÇÃO CIENTÍFICA
    projeto_ic = Projeto.objects.create(
        tema="Projeto de IC",
        tipo=Projeto.TipoPesquisa.INICIACAO_CIENTIFICA, # <-- O ponto chave
        resumo="Resumo...",
        duracao=12
    )
    
    # Associa o PRIMEIRO aluno (isso deve funcionar)
    associate_aluno_to_project(
        project_id=projeto_ic.id_proj, 
        aluno_id=aluno1.id_aluno
    )
    
    # Garante que o primeiro aluno foi associado
    projeto_ic.refresh_from_db()
    assert projeto_ic.alunos.count() == 1

    # 2. ACT & 3. ASSERT
    # Tenta associar o SEGUNDO aluno ao mesmo projeto de IC
    with pytest.raises(ValidationError) as e:
        associate_aluno_to_project(
            project_id=projeto_ic.id_proj, 
            aluno_id=aluno2.id_aluno
        )
    
    # Verifica a mensagem de erro
    assert "só podem ter um aluno ativo" in str(e.value)
    
    # Garante que o segundo aluno não foi associado
    projeto_ic.refresh_from_db()
    assert projeto_ic.alunos.count() == 1