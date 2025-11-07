# core/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Professor, Aluno, Projeto, Departamento, Curso, ProfessorLattes, HistAluno,
    AlunoProj, Orientador, Assessor
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

class ProfessorSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_professor = serializers.CharField(read_only=True)
    
    departamento = serializers.CharField(source='departamento.nome_departamento', read_only=True)
    lattes_link = serializers.SerializerMethodField()
    class Meta:
        model = Professor
        fields = ['id_professor', 'nome', 'departamento', 'email', 'link_citations', 'lattes_link']
    def get_lattes_link(self, obj):
        try: return obj.professorlattes.link
        except ProfessorLattes.DoesNotExist: return None

class AlunoSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_aluno = serializers.CharField(read_only=True)

    curso = serializers.CharField(source='curso.nome', read_only=True)
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso', write_only=True
    )
    class Meta:
        model = Aluno
        fields = ['id_aluno', 'nome', 'email', 'curso', 'curso_id', 'telefone']

class ProfessorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'departamento']

# --- ProfessorLattesSerializer ---
class ProfessorLattesSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # O campo 'professor' (ForeignKey) é serializado como seu ID.
    # Força esse ID grande a ser enviado como String (texto).
    professor = serializers.CharField()

    class Meta:
        model = ProfessorLattes
        fields = ['professor', 'cod_lattes', 'subarea', 'link', 'palavras_chave']

class AlunoProjStatusSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_aluno = serializers.CharField(source='aluno.id_aluno', read_only=True)
    nome_aluno = serializers.CharField(source='aluno.nome', read_only=True)
    class Meta:
        model = AlunoProj
        fields = ['id_aluno', 'nome_aluno', 'ativo']

class OrientadorStatusSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_professor = serializers.CharField(source='professor.id_professor', read_only=True)
    nome_professor = serializers.CharField(source='professor.nome', read_only=True)
    class Meta:
        model = Orientador
        fields = ['id_professor', 'nome_professor', 'ativo']

class AssessorStatusSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_professor = serializers.CharField(source='professor.id_professor', read_only=True)
    nome_professor = serializers.CharField(source='professor.nome', read_only=True)
    class Meta:
        model = Assessor
        fields = ['id_professor', 'nome_professor', 'ativo']

class ProjetoSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO 1 ---
    # Força o ID grande a ser enviado como String (texto)
    id_proj = serializers.CharField(read_only=True)
    
    pendencia_display = serializers.CharField(source='get_pendencia_display', read_only=True)
    alunos_status = AlunoProjStatusSerializer(many=True, read_only=True, source='alunoproj_set')
    orientadores_status = OrientadorStatusSerializer(many=True, read_only=True, source='orientador_set')
    assessores_status = AssessorStatusSerializer(many=True, read_only=True, source='assessor_set')
    class Meta:
        model = Projeto
        fields = [
            'id_proj', 'tema', 'tipo', 'resumo', 'palavra_chave', 'duracao',
            'bolsa',
            'pendencia',
            'pendencia_display',
            'orientadores_status', 'assessores_status', 'alunos_status',
            'mongo_id',
            'melhor_corretor'
        ]
        # --- CORREÇÃO 2 ---
        # Remove 'id_proj' desta lista, pois já foi definido acima
        read_only_fields = ['pendencia_display', 'orientadores_status', 'assessores_status', 'alunos_status', 'melhor_corretor']

class HistAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistAluno
        fields = ['cod_disciplina', 'aprovado']

class DepartamentoSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_departamento = serializers.CharField(read_only=True)

    class Meta:
        model = Departamento
        fields = ['id_departamento', 'nome_departamento']

class ProfessorLattesKeywordsSerializer(serializers.ModelSerializer):
    # --- CORREÇÃO ---
    # Força o ID grande a ser enviado como String (texto)
    id_professor = serializers.CharField(source='professor.id_professor', read_only=True)
    class Meta:
        model = ProfessorLattes
        fields = ['id_professor', 'palavras_chave']