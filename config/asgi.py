"""
ASGI config for config project. (Nome do projeto atualizado)

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# --- ALTERAÇÃO AQUI ---
# MUDOU DE "api_faculdade.settings" para "config.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()