# .mutmut_config.py
import os
import sys
import traceback
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent

def _append_log(text):
    try:
        with open(PROJECT_ROOT / "mutmut_debug.log", "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        # não falhar aqui
        pass

def pre_mutation(context):
    try:
        # garantir execução na raiz do projeto
        os.chdir(PROJECT_ROOT)

        # variáveis Django / path
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
        os.environ.setdefault("PYTHONPATH", str(PROJECT_ROOT))

        # forçar comando de teste explícito
        context.config.test_command = (
            f"pytest {PROJECT_ROOT / 'tests'} --ds=config.settings -q --disable-warnings --maxfail=1"
        )

        # registrar estado
        _append_log("=== pre_mutation ===")
        _append_log(f"time: {datetime.utcnow().isoformat()}Z")
        _append_log(f"cwd: {os.getcwd()}")
        _append_log(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        _append_log(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
        _append_log(f"sys.executable: {sys.executable}")
        _append_log(f"sys.path (len={len(sys.path)}):")
        for p in sys.path[:30]:
            _append_log(f"  {p}")
        _append_log(f"test_command: {context.config.test_command}")
        # listar alguns arquivos .py no projeto (até 50)
        py_files = list(PROJECT_ROOT.glob("**/*.py"))[:50]
        _append_log(f"found_py_count: {len(py_files)} (showing up to 50):")
        for p in py_files:
            _append_log(f"  {p.relative_to(PROJECT_ROOT)}")
        _append_log(f"context: {repr(context)[:200]}")
        _append_log("")  # separador
    except Exception:
        _append_log("pre_mutation EXCEPTION:")
        _append_log(traceback.format_exc())

def post_mutation(context):
    try:
        _append_log("=== post_mutation ===")
        _append_log(f"time: {datetime.utcnow().isoformat()}Z")
        _append_log("")  # separador
    except Exception:
        pass
