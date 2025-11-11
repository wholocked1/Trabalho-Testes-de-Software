# Descrição do Projeto: Sistema de Gestão de Projetos Acadêmicos

## 1. Tema do Projeto

O projeto é um sistema de gerenciamento de projetos acadêmicos (Iniciação Científica, TCC, etc.) para uma instituição de ensino. Ele permite o cadastro de alunos, professores e projetos, e gerencia a associação entre eles (orientadores, assessores, etc.).

O tema se enquadra no domínio de "Sistema de gerenciamento" sugerido no escopo do trabalho.

## 2. Características Técnicas e Arquitetura

O projeto foi construído em Python utilizando o framework Django e segue as características técnicas obrigatórias de arquitetura e estrutura.

### Modularização

O código-fonte está organizado no pacote `src/core`, com sub-módulos para cada responsabilidade:
* `models.py`: Define a estrutura de dados (entidades).
* `repositories.py`: Implementa o *Repository Pattern* para acesso a dados.
* `services.py`: Contém a lógica de negócio (regras e orquestração).
* `serializers.py`: Define a representação JSON dos dados para a API.
* `views.py`: Expõe os dados e a lógica de negócio como uma API REST.

### Separação de Responsabilidades (Arquitetura em Camadas)

O projeto segue uma arquitetura em camadas bem definida, separando as responsabilidades:

1.  **Camada de Apresentação (API):** Implementada em `views.py` e `serializers.py` usando o **Django REST Framework**. Esta camada é responsável por receber requisições HTTP, serializar dados e retornar respostas JSON.
2.  **Camada de Lógica de Negócio:** Implementada em `services.py`. Esta camada orquestra as operações e contém as regras de negócio (ex: `create_project_with_associations`, `deactivate_project_participant`). Ela não acessa o banco diretamente, dependendo da camada de repositório.
3.  **Camada de Acesso a Dados (Repository):** Implementada em `repositories.py`. Esta camada isola todas as consultas ao banco de dados (ORM do Django), fornecendo funções simples (`get_professor_by_id`, `create_project`, etc.) para a camada de serviço.

### Injeção de Dependências

A injeção de dependências é utilizada na camada de serviços (`services.py`), que depende das funções do repositório (`repositories.py`).

Isso é demonstrado nos testes unitários (`test_services.py`), onde a camada de repositório é substituída por *mocks* (usando `pytest-mock`). Isso permite testar a lógica de negócio (`services.py`) de forma isolada, sem tocar no banco de dados, cumprindo o requisito de facilitar testes com mocks.

## 3. Funcionalidades Mínimas Implementadas

O projeto cumpre os requisitos de funcionalidades mínimas:

#### 5 Operações CRUD
O projeto implementa 5 operações CRUD no *endpoint* `/api/projetos/`, como demonstrado nos testes funcionais do Postman:
1.  **Create:** `POST /api/projetos/`
2.  **Read (List):** `GET /api/projetos/`
3.  **Read (Retrieve):** `GET /api/projetos/{id}/`
4.  **Update:** `PUT /api/projetos/{id}/` (ou `PATCH`)
5.  **Delete:** `DELETE /api/projetos/{id}/`

#### 3 Regras de Negócio Complexas
Pelo menos 3 regras de negócio complexas foram implementadas e testadas:

1.  **Criação de Projeto com Associações (Orquestração):** A função `create_project_with_associations` (em `services.py`) orquestra múltiplas operações: valida os dados, cria um `Projeto` e, em seguida, cria as associações `Orientador` e `AlunoProj`, garantindo que o projeto seja criado com seus participantes principais.
2.  **Validação de Múltiplos Alunos em IC (Validação de Múltiplas Condições):** O modelo `AlunoProj` contém lógica no método `.save()` que verifica (1) se o projeto é de Iniciação Científica e (2) se já existe outro aluno ativo. Se ambas as condições forem verdadeiras, uma `ValidationError` é lançada, impedindo a associação.
3.  **Contagem de Projetos do Professor (Cálculo/Processamento):** O *endpoint* `GET /api/professores/{id}/contagem-projetos/` (implementado em `services.py`) calcula e retorna o número de orientações e assessorias ativas de um professor, consultando diferentes tabelas de associação.

#### 2 Funcionalidades de Consulta com Filtros
A listagem de projetos (`GET /api/projetos/`) implementa filtros de consulta, como demonstrado nos testes da API e implementado em `views.py`:
1.  `GET /api/projetos/?orientador_id=X` (Filtra projetos por um orientador específico).
2.  `GET /api/projetos/?pendencia=pendente` (Filtra projetos por status de pendência).

## 4. Persistência de Dados

* **Banco de Dados:** O projeto utiliza **CockroachDB** (compatível com PostgreSQL), como configurado em `settings.py`.
* **Camada de Acesso:** O acesso aos dados é gerenciado através do **Repository Pattern** (implementado em `repositories.py`).

## 5. Interface

A interface principal é uma **API REST**, construída com **Django REST Framework**, conforme demonstrado pelos *endpoints* testados no Postman.
