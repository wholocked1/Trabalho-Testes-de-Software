# core/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Professor, Aluno, Projeto, Departamento, Curso, ProfessorLattes, HistAluno,
    AlunoProj, Orientador, Assessor
)

class ProfessorSerializer(serializers.ModelSerializer):
    departamento = serializers.CharField(source='departamento.nome_departamento', read_only=True)
    lattes_link = serializers.SerializerMethodField()
    class Meta:
        model = Professor
        fields = ['id_professor', 'nome', 'departamento', 'email', 'link_citations', 'lattes_link']
    def get_lattes_link(self, obj):
        try: return obj.professorlattes.link
        except ProfessorLattes.DoesNotExist: return None

class AlunoSerializer(serializers.ModelSerializer):
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

# --- ProfessorLattesSerializer CORRECTED ---
class ProfessorLattesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorLattes
        # Corrected: 'nome' field removed from the list
        fields = ['professor', 'cod_lattes', 'subarea', 'link', 'palavras_chave']

class AlunoProjStatusSerializer(serializers.ModelSerializer):
    id_aluno = serializers.IntegerField(source='aluno.id_aluno', read_only=True)
    nome_aluno = serializers.CharField(source='aluno.nome', read_only=True)
    class Meta:
        model = AlunoProj
        fields = ['id_aluno', 'nome_aluno', 'ativo']

class OrientadorStatusSerializer(serializers.ModelSerializer):
    id_professor = serializers.IntegerField(source='professor.id_professor', read_only=True)
    nome_professor = serializers.CharField(source='professor.nome', read_only=True)
    class Meta:
        model = Orientador
        fields = ['id_professor', 'nome_professor', 'ativo']

class AssessorStatusSerializer(serializers.ModelSerializer):
    id_professor = serializers.IntegerField(source='professor.id_professor', read_only=True)
    nome_professor = serializers.CharField(source='professor.nome', read_only=True)
    class Meta:
        model = Assessor
        fields = ['id_professor', 'nome_professor', 'ativo']

class ProjetoSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['id_proj', 'pendencia_display', 'orientadores_status', 'assessores_status', 'alunos_status', 'melhor_corretor']

class HistAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistAluno
        fields = ['cod_disciplina', 'aprovado']

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id_departamento', 'nome_departamento']

class ProfessorLattesKeywordsSerializer(serializers.ModelSerializer):
    id_professor = serializers.IntegerField(source='professor.id_professor', read_only=True)
    class Meta:
        model = ProfessorLattes
        fields = ['id_professor', 'palavras_chave']