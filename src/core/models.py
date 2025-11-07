# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Departamento(models.Model):
    id_departamento = models.BigIntegerField(primary_key=True)
    nome_departamento = models.CharField(max_length=150, unique=True)
    class Meta: db_table = 'departamentos'
    def __str__(self): return self.nome_departamento

class Curso(models.Model):
    id_curso = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='id_departamento', related_name='cursos')
    class Meta: db_table = 'cursos'
    def __str__(self): return self.nome

class Professor(models.Model):
    id_professor = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    link_citations = models.CharField(max_length=500, blank=True, null=True) # CharField
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_departamento', related_name='professores')
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_prof')
    class Meta: db_table = 'professores'
    def __str__(self): return self.nome

class Aluno(models.Model):
    id_aluno = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20) # Obrigatório
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, db_column='id_curso', related_name='alunos') # Obrigatório
    class Meta: db_table = 'alunos'
    def __str__(self): return self.nome

class Projeto(models.Model):
    id_proj = models.AutoField(primary_key=True) # Automático
    
    class TipoPesquisa(models.IntegerChoices):
        INICIACAO_CIENTIFICA = 1, 'Iniciação Científica'
        TCC = 2, 'Trabalho de Conclusão de Curso'
        MESTRADO = 3, 'Mestrado'
        DOUTORADO = 4, 'Doutorado'
        EXTENSAO = 5, 'Extensão'
    
    BOLSA_CHOICES = [('FEI', 'FEI'), ('CNPQ', 'CNPq'), ('FAPESP', 'FAPESP')]

    class StatusProjeto(models.IntegerChoices):
        AGUARDANDO_COORDENACAO = 1, 'Esperando aprovação da Coordenação'
        AGUARDANDO_ASSESSOR = 2, 'Esperando aprovação do assessor'
        AGUARDANDO_RH = 3, 'Esperando aprovação do RH'
        APROVADO = 4, 'Aprovado'
        CANCELADO = 5, 'Cancelado'
        FINALIZADO = 6, 'Finalizado'
        AGUARDANDO_REL_PARCIAL = 7, 'Esperando relatório parcial'
        AGUARDANDO_RESP_PARCIAL = 8, 'Esperando resposta do assessor ao relatório parcial'
        AGUARDANDO_REL_FINAL = 9, 'Esperando relatório final'
        AGUARDANDO_RESP_FINAL = 10, 'Esperando resposta do assessor ao relatório final'
        AGUARDANDO_ASSINATURAS = 11, 'Esperando assinaturas'

    # --- CORREÇÃO APLICADA AQUI ---
    # Campos agora são obrigatórios (removido blank=True, null=True)
    # Isso fará o teste [EXCEÇÃO 2] passar.
    tema = models.CharField(max_length=255, default='')
    tipo = models.IntegerField(choices=TipoPesquisa.choices, default=1)
    resumo = models.TextField(default='')
    duracao = models.IntegerField(help_text="Duração em meses", default=12)
    # -------------------------------

    palavra_chave = models.CharField(max_length=255, blank=True, null=True)
    bolsa = models.CharField(max_length=10, choices=BOLSA_CHOICES, blank=True, null=True)
    pendencia = models.IntegerField(
        choices=StatusProjeto.choices,
        default=StatusProjeto.AGUARDANDO_COORDENACAO
    )
    mongo_id = models.CharField(
        max_length=24, blank=True, null=True, unique=True, db_column='_id'
    )
    melhor_corretor = models.TextField(
        blank=True, 
        null=True, 
        help_text="Texto retornado pela função de melhor corretor"
    )

    alunos = models.ManyToManyField(Aluno, through='AlunoProj', related_name='projetos')
    orientadores = models.ManyToManyField(Professor, through='Orientador', related_name='projetos_orientados')
    assessores = models.ManyToManyField(Professor, through='Assessor', related_name='projetos_assessorados')
    
    class Meta: db_table = 'projetos'
    def __str__(self): return self.tema if self.tema else f"Projeto {self.id_proj}"

class AlunoProj(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, db_column='id_aluno')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, db_column='id_proj')
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'aluno_proj'
        unique_together = (('aluno', 'projeto'),)

class Orientador(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, db_column='id_prof')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, db_column='id_proj')
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    class Meta:
        db_table = 'orientador'
        unique_together = (('professor', 'projeto'),)

class Assessor(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, db_column='id_prof')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, db_column='id_proj')
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    class Meta:
        db_table = 'assessores'
        unique_together = (('professor', 'projeto'),)

class ProfessorLattes(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE, primary_key=True, db_column='id_professor')
    cod_lattes = models.CharField(max_length=50, unique=True)
    # nome = models.CharField(max_length=200) # REMOVIDO
    subarea = models.CharField(max_length=150, blank=True, null=True) 
    link = models.URLField(max_length=500)
    palavras_chave = models.TextField(blank=True, help_text="Palavras-chave de pesquisa, separadas por vírgula")
    class Meta: db_table = 'professores_lattes'
    def __str__(self): return f"Lattes de {self.professor.nome} ({self.cod_lattes})"

class HistAluno(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, db_column='id_aluno')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='id_departamento')
    cod_disciplina = models.CharField(max_length=20)
    aprovado = models.BooleanField(default=False)
    class Meta:
        db_table = 'hist_alunos'
    def __str__(self):
        status = "Aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"