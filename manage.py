#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # --- INÍCIO DAS ALTERAÇÕES ---

    # 1. Adiciona o 'src' ao Python Path
    # Pega o diretório onde o manage.py está (a raiz do projeto)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Adiciona a pasta 'src' (que está em BASE_DIR/src) ao path
    sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

    # 2. Altera o caminho dos settings
    # MUDOU DE "api_faculdade.settings" para "config.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # --- FIM DAS ALTERAÇÕES ---

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()