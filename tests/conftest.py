# tests/conftest.py
import pytest
from django.db import connection

@pytest.fixture(scope='session', autouse=True)
def set_cockroachdb_schema(django_db_setup, django_db_blocker):
    """
    Força a conexão de teste a usar o schema 'faculdade' ANTES de tudo.
    Isso corrige o bug 'ProgrammingError: no database or schema specified'.
    """
    # Desbloqueia o acesso ao BD para esta fixture
    with django_db_blocker.unblock():
        try:
            # Pega a conexão e define o schema
            with connection.cursor() as cursor:
                cursor.execute("SET search_path = faculdade;")
        except Exception as e:
            # Se a conexão falhar por algum motivo, mostre o erro
            print(f"Falha ao definir o search_path: {e}")
            pass