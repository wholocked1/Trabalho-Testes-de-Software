# Plano de Testes: Sistema de Gestão de Projetos Académicos

## 1. Introdução

Este documento descreve o plano de testes para o "Sistema de Gestão de Projetos Académicos", em conformidade com os requisitos da disciplina de Simulação e Teste de Software (CC8550).

A estratégia de testes foca-se em validar o sistema em múltiplas camadas, utilizando uma combinação de testes de caixa-branca (Unitários, Integração), caixa-preta (Funcionais/API) e testes estruturais (Cobertura e Mutação).

## 2. Estratégia e Ferramentas

| Categoria de Teste | Ferramenta Utilizada | Ficheiro de Configuração |
| :--- | :--- | :--- |
| Testes Unitários | `pytest` + `pytest-mock` | `pytest.ini` |
| Testes de Integração | `pytest` + `pytest-django` | `pytest.ini` |
| Testes Funcionais (API) | `Postman` | `testes_postman.json` |
| Testes Estruturais | `pytest-cov` | `pytest.ini` |
| Testes de Mutação | `Cosmic-Ray` | `cosmic-ray.toml` |

---

## 3. Categorias de Teste Planeadas

### 3.1. Testes Unitários (Peso: 25%)

* **Objetivo:** Testar a camada de Lógica de Negócio (`services.py`) de forma completamente isolada.
* **Requisito:** Mínimo de 30 casos de teste.
* **Implementação:**
    * Os testes estão localizados em `tests/unit/test_services.py`.
    * Utiliza-se `pytest-mock` para simular (mock) a camada de `repositories.py`.
    * Isto garante que a lógica de negócio (ex: validações, manipulação de dados) é testada sem qualquer acesso real ao banco de dados.
    * Os testes cobrem caminhos felizes (sucesso) e caminhos de erro (ex: `_not_found`, `_fails_if_...`).

### 3.2. Testes de Integração (Peso: 20%)

* **Objetivo:** Testar o fluxo completo desde a camada de serviço (`services.py`) até à camada de acesso a dados (`repositories.py`) e ao banco de dados real (CockroachDB).
* **Requisito:** Mínimo de 10 testes de integração.
* **Implementação:**
    * Os testes estão localizados em `tests/integration/test_integration_services.py`.
    * Utiliza-se a marcação `pytest.mark.django_db` para criar e destruir um banco de dados de teste para cada execução.
    * Uma *fixture* (`setup_database_data`) popula o banco com dados de pré-requisito (Departamentos, Cursos, Professores, Alunos).
    * Estes testes validam que a lógica de negócio funciona corretamente quando integrada com o ORM do Django e que as regras de negócio nos `models.py` (ex: validações de `save()`) são acionadas.

### 3.3. Testes Funcionais (Caixa-Preta) (Peso: 15%)

* **Objetivo:** Testar a API REST (a camada de `views.py`) como um utilizador final, focando apenas em entradas (requests HTTP) e saídas (respostas JSON).
* **Requisito:** Mínimo de 8 cenários funcionais, incluindo regras de negócio.
* **Implementação:**
    * Os testes foram criados e executados com o **Postman**.
    * O relatório de execução (`CC8550 - Testes de API...json`) comprova a execução bem-sucedida de 22 testes.
    * Os cenários incluem:
        1.  O fluxo CRUD completo (Create, Read, Update, Delete) para `/api/projetos/`.
        2.  Testes de regras de negócio (ex: associar assessor, desativar participante, contagem de projetos).
        3.  Testes de filtros (ex: `?orientador_id=X`).
        4.  Testes de exceções (ex: 404 Not Found, 400 Bad Request).

### 3.4. Testes Estruturais (Cobertura) (Peso: 15%)

* **Objetivo:** Garantir que a suíte de testes (unitários e integração) exercita uma percentagem mínima do código-fonte.
* **Requisito:** Mínimo de 80% de cobertura de código.
* **Implementação:**
    * A ferramenta `pytest-cov` é utilizada para medir a cobertura.
    * O comando de execução é `pytest --cov=src.core`.
    * A cobertura é focada nos módulos de lógica de negócio (`services.py`, `repositories.py`, `models.py`).

### 3.5. Testes de Mutação (Peso: 10%)

* **Objetivo:** Avaliar a qualidade e eficácia da suíte de testes, verificando se os testes falham quando o código-fonte sofre pequenas alterações (mutações).
* **Requisito:** Usar `mutmut` (ou alternativa, com justificação) e analisar os resultados.
* **Implementação:**
    * **Ferramenta:** Foi utilizado o **Cosmic-Ray**, pois o `mutmut` (solicitado no escopo) revelou-se incompatível com o ambiente de desenvolvimento Windows (devido a uma dependência da biblioteca `resource`, exclusiva do Linux).
    * A configuração (`cosmic-ray.toml`) foi ajustada para focar as mutações apenas nos módulos de *backend* (`src/core`) e executar apenas os testes de integração (`-m django_db`), que são os únicos com acesso ao banco de dados.
    * A análise dos mutantes sobreviventes será detalhada no `relatorio_testes.md`.

### 3.6. Testes Específicos (Peso: 15%)

O escopo exige pelo menos 2 dos 5 tipos de testes específicos. Este projeto implementa 3:

1.  **Testes de API/REST:** Concluído através dos Testes Funcionais com Postman.
2.  **Testes com Mocks e Stubs:** Concluído através dos Testes Unitários com `pytest-mock`.
3.  **Testes de Exceções:** Concluído através dos Testes Unitários (ex: `pytest.raises(ObjectDoesNotExist)`) e dos Testes de API (ex: validação de status 400).
