# core/admin.py

from django.contrib import admin
from .models import (
    Departamento,
    Curso,
    Professor,
    Aluno,
    Projeto,
    AlunoProj,
    Orientador,
    Assessor,
    ProfessorLattes,
    HistAluno
)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_departamento', 'id_departamento')
    search_fields = ('nome_departamento',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('nome', 'id_curso')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'departamento', 'id_professor')
    list_filter = ('departamento',)
    search_fields = ('nome', 'email', 'id_professor')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'curso', 'id_aluno')
    list_filter = ('curso__departamento', 'curso')
    search_fields = ('nome', 'email', 'id_aluno')
    autocomplete_fields = ['curso']

class AlunoProjInline(admin.TabularInline):
    model = AlunoProj
    extra = 1
    autocomplete_fields = ['aluno']
    fields = ('aluno', 'ativo', 'datainicio')

class OrientadorInline(admin.TabularInline):
    model = Orientador
    extra = 1
    autocomplete_fields = ['professor']
    fields = ('professor', 'ativo', 'datainicio')

class AssessorInline(admin.TabularInline):
    model = Assessor
    extra = 0
    autocomplete_fields = ['professor']
    fields = ('professor', 'ativo', 'datainicio')

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    # Corrected list_display to include the editable field 'pendencia'
    list_display = ('tema', 'get_tipo_display', 'pendencia', 'bolsa', 'id_proj')
    list_filter = ('tipo', 'pendencia', 'bolsa')
    search_fields = ('tema', 'palavra_chave', 'resumo', 'id_proj')
    list_editable = ('pendencia',) # Now valid
    inlines = [OrientadorInline, AlunoProjInline, AssessorInline]

@admin.register(ProfessorLattes)
class ProfessorLattesAdmin(admin.ModelAdmin):
    list_display = ('professor', 'cod_lattes', 'subarea', 'link')
    search_fields = ('professor__nome', 'cod_lattes', 'subarea', 'palavras_chave')
    autocomplete_fields = ['professor']

@admin.register(HistAluno)
class HistAlunoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'cod_disciplina', 'departamento', 'aprovado')
    list_filter = ('departamento', 'aprovado')
    search_fields = ('aluno__nome', 'cod_disciplina')
    autocomplete_fields = ['aluno', 'departamento']

# admin.site.register(AlunoProj)
# admin.site.register(Orientador)
# admin.site.register(Assessor)