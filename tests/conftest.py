# # tests/conftest.py
# import pytest
# from django.db.backends.postgresql.base import DatabaseWrapper

# # Armazena o método original para podermos restaurá-lo depois
# _original_get_connection_params = DatabaseWrapper.get_connection_params

# @pytest.fixture(scope='session', autouse=True)
# def patch_cockroachdb_connection():
#     """
#     Força o 'search_path=faculdade' em todas as conexões de teste.
    
#     Isso "monkeypatches" o driver do Django para injetar a configuração
#     de schema antes que o pytest-django tente criar o banco de dados,
#     corrigindo o erro 'no database or schema specified'.
#     """
    
#     def new_get_connection_params(self):
#         # Chama o método original para obter os parâmetros (user, host, etc.)
#         params = _original_get_connection_params(self)
        
#         # Adiciona/sobrescreve o 'search_path'
#         # Pega quaisquer 'options' que já existam e adiciona a nossa
#         existing_options = params.get('options', '')
#         params['options'] = f"-c search_path=faculdade {existing_options}".strip()
        
#         return params
    
#     # Aplica o patch
#     DatabaseWrapper.get_connection_params = new_get_connection_params
    
#     # Permite que a sessão de teste rode com o patch aplicado
#     yield
    
#     # Desfaz o patch após a sessão de teste terminar
#     DatabaseWrapper.get_connection_params = _original_get_connection_params