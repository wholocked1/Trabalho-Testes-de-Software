# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
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
    tema = models.CharField(max_length=255)
    tipo = models.IntegerField(choices=TipoPesquisa.choices)
    resumo = models.TextField()
    duracao = models.IntegerField(help_text="Duração em meses")
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

    def xǁAlunoProjǁsave__mutmut_orig(self, *args, **kwargs):
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

    def xǁAlunoProjǁsave__mutmut_1(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') or self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_2(self, *args, **kwargs):
        if self.ativo or hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_3(self, *args, **kwargs):
        if self.ativo and hasattr(None, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_4(self, *args, **kwargs):
        if self.ativo and hasattr(self, None) and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_5(self, *args, **kwargs):
        if self.ativo and hasattr('projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_6(self, *args, **kwargs):
        if self.ativo and hasattr(self, ) and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_7(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'XXprojetoXX') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_8(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'PROJETO') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_9(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = None
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_10(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=None).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_11(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto != Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_12(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=None).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_13(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=None, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_14(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=None).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_15(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_16(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_17(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=False).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_18(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError(None)
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_19(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("XXProjetos de Iniciação Científica só podem ter um aluno ativo por vez.XX")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_20(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("projetos de iniciação científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_21(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("PROJETOS DE INICIAÇÃO CIENTÍFICA SÓ PODEM TER UM ALUNO ATIVO POR VEZ.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, **kwargs)

    def xǁAlunoProjǁsave__mutmut_22(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(**kwargs)

    def xǁAlunoProjǁsave__mutmut_23(self, *args, **kwargs):
        if self.ativo and hasattr(self, 'projeto') and self.projeto_id: # Checa se o projeto existe
             # Acessa o tipo do projeto de forma segura
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if AlunoProj.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um aluno ativo por vez.")
             except Projeto.DoesNotExist:
                 pass # Ou levante um erro se o projeto não existir
        super().save(*args, )
    
    xǁAlunoProjǁsave__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAlunoProjǁsave__mutmut_1': xǁAlunoProjǁsave__mutmut_1, 
        'xǁAlunoProjǁsave__mutmut_2': xǁAlunoProjǁsave__mutmut_2, 
        'xǁAlunoProjǁsave__mutmut_3': xǁAlunoProjǁsave__mutmut_3, 
        'xǁAlunoProjǁsave__mutmut_4': xǁAlunoProjǁsave__mutmut_4, 
        'xǁAlunoProjǁsave__mutmut_5': xǁAlunoProjǁsave__mutmut_5, 
        'xǁAlunoProjǁsave__mutmut_6': xǁAlunoProjǁsave__mutmut_6, 
        'xǁAlunoProjǁsave__mutmut_7': xǁAlunoProjǁsave__mutmut_7, 
        'xǁAlunoProjǁsave__mutmut_8': xǁAlunoProjǁsave__mutmut_8, 
        'xǁAlunoProjǁsave__mutmut_9': xǁAlunoProjǁsave__mutmut_9, 
        'xǁAlunoProjǁsave__mutmut_10': xǁAlunoProjǁsave__mutmut_10, 
        'xǁAlunoProjǁsave__mutmut_11': xǁAlunoProjǁsave__mutmut_11, 
        'xǁAlunoProjǁsave__mutmut_12': xǁAlunoProjǁsave__mutmut_12, 
        'xǁAlunoProjǁsave__mutmut_13': xǁAlunoProjǁsave__mutmut_13, 
        'xǁAlunoProjǁsave__mutmut_14': xǁAlunoProjǁsave__mutmut_14, 
        'xǁAlunoProjǁsave__mutmut_15': xǁAlunoProjǁsave__mutmut_15, 
        'xǁAlunoProjǁsave__mutmut_16': xǁAlunoProjǁsave__mutmut_16, 
        'xǁAlunoProjǁsave__mutmut_17': xǁAlunoProjǁsave__mutmut_17, 
        'xǁAlunoProjǁsave__mutmut_18': xǁAlunoProjǁsave__mutmut_18, 
        'xǁAlunoProjǁsave__mutmut_19': xǁAlunoProjǁsave__mutmut_19, 
        'xǁAlunoProjǁsave__mutmut_20': xǁAlunoProjǁsave__mutmut_20, 
        'xǁAlunoProjǁsave__mutmut_21': xǁAlunoProjǁsave__mutmut_21, 
        'xǁAlunoProjǁsave__mutmut_22': xǁAlunoProjǁsave__mutmut_22, 
        'xǁAlunoProjǁsave__mutmut_23': xǁAlunoProjǁsave__mutmut_23
    }
    
    def save(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAlunoProjǁsave__mutmut_orig"), object.__getattribute__(self, "xǁAlunoProjǁsave__mutmut_mutants"), args, kwargs, self)
        return result 
    
    save.__signature__ = _mutmut_signature(xǁAlunoProjǁsave__mutmut_orig)
    xǁAlunoProjǁsave__mutmut_orig.__name__ = 'xǁAlunoProjǁsave'

    class Meta:
        db_table = 'aluno_proj'
        unique_together = (('aluno', 'projeto'),)

class Orientador(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, db_column='id_prof')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, db_column='id_proj')
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField(default=timezone.now)

    def xǁOrientadorǁsave__mutmut_orig(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_1(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') or self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_2(self, *args, **kwargs):
         if self.ativo or hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_3(self, *args, **kwargs):
         if self.ativo and hasattr(None, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_4(self, *args, **kwargs):
         if self.ativo and hasattr(self, None) and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_5(self, *args, **kwargs):
         if self.ativo and hasattr('projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_6(self, *args, **kwargs):
         if self.ativo and hasattr(self, ) and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_7(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'XXprojetoXX') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_8(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'PROJETO') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_9(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = None
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_10(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=None).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_11(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto != Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_12(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=None).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_13(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=None, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_14(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=None).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_15(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_16(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_17(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=False).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_18(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError(None)
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_19(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("XXProjetos de Iniciação Científica só podem ter um orientador ativo por vez.XX")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_20(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("projetos de iniciação científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_21(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("PROJETOS DE INICIAÇÃO CIENTÍFICA SÓ PODEM TER UM ORIENTADOR ATIVO POR VEZ.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁOrientadorǁsave__mutmut_22(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(**kwargs)

    def xǁOrientadorǁsave__mutmut_23(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Orientador.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um orientador ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, )
    
    xǁOrientadorǁsave__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrientadorǁsave__mutmut_1': xǁOrientadorǁsave__mutmut_1, 
        'xǁOrientadorǁsave__mutmut_2': xǁOrientadorǁsave__mutmut_2, 
        'xǁOrientadorǁsave__mutmut_3': xǁOrientadorǁsave__mutmut_3, 
        'xǁOrientadorǁsave__mutmut_4': xǁOrientadorǁsave__mutmut_4, 
        'xǁOrientadorǁsave__mutmut_5': xǁOrientadorǁsave__mutmut_5, 
        'xǁOrientadorǁsave__mutmut_6': xǁOrientadorǁsave__mutmut_6, 
        'xǁOrientadorǁsave__mutmut_7': xǁOrientadorǁsave__mutmut_7, 
        'xǁOrientadorǁsave__mutmut_8': xǁOrientadorǁsave__mutmut_8, 
        'xǁOrientadorǁsave__mutmut_9': xǁOrientadorǁsave__mutmut_9, 
        'xǁOrientadorǁsave__mutmut_10': xǁOrientadorǁsave__mutmut_10, 
        'xǁOrientadorǁsave__mutmut_11': xǁOrientadorǁsave__mutmut_11, 
        'xǁOrientadorǁsave__mutmut_12': xǁOrientadorǁsave__mutmut_12, 
        'xǁOrientadorǁsave__mutmut_13': xǁOrientadorǁsave__mutmut_13, 
        'xǁOrientadorǁsave__mutmut_14': xǁOrientadorǁsave__mutmut_14, 
        'xǁOrientadorǁsave__mutmut_15': xǁOrientadorǁsave__mutmut_15, 
        'xǁOrientadorǁsave__mutmut_16': xǁOrientadorǁsave__mutmut_16, 
        'xǁOrientadorǁsave__mutmut_17': xǁOrientadorǁsave__mutmut_17, 
        'xǁOrientadorǁsave__mutmut_18': xǁOrientadorǁsave__mutmut_18, 
        'xǁOrientadorǁsave__mutmut_19': xǁOrientadorǁsave__mutmut_19, 
        'xǁOrientadorǁsave__mutmut_20': xǁOrientadorǁsave__mutmut_20, 
        'xǁOrientadorǁsave__mutmut_21': xǁOrientadorǁsave__mutmut_21, 
        'xǁOrientadorǁsave__mutmut_22': xǁOrientadorǁsave__mutmut_22, 
        'xǁOrientadorǁsave__mutmut_23': xǁOrientadorǁsave__mutmut_23
    }
    
    def save(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrientadorǁsave__mutmut_orig"), object.__getattribute__(self, "xǁOrientadorǁsave__mutmut_mutants"), args, kwargs, self)
        return result 
    
    save.__signature__ = _mutmut_signature(xǁOrientadorǁsave__mutmut_orig)
    xǁOrientadorǁsave__mutmut_orig.__name__ = 'xǁOrientadorǁsave'

    class Meta:
        db_table = 'orientador'
        unique_together = (('professor', 'projeto'),)

class Assessor(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, db_column='id_prof')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, db_column='id_proj')
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField(default=timezone.now)

    def xǁAssessorǁsave__mutmut_orig(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_1(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') or self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_2(self, *args, **kwargs):
         if self.ativo or hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_3(self, *args, **kwargs):
         if self.ativo and hasattr(None, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_4(self, *args, **kwargs):
         if self.ativo and hasattr(self, None) and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_5(self, *args, **kwargs):
         if self.ativo and hasattr('projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_6(self, *args, **kwargs):
         if self.ativo and hasattr(self, ) and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_7(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'XXprojetoXX') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_8(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'PROJETO') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_9(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = None
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_10(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=None).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_11(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto != Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_12(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=None).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_13(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=None, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_14(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=None).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_15(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_16(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_17(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=False).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_18(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError(None)
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_19(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("XXProjetos de Iniciação Científica só podem ter um assessor ativo por vez.XX")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_20(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("projetos de iniciação científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_21(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("PROJETOS DE INICIAÇÃO CIENTÍFICA SÓ PODEM TER UM ASSESSOR ATIVO POR VEZ.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, **kwargs)

    def xǁAssessorǁsave__mutmut_22(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(**kwargs)

    def xǁAssessorǁsave__mutmut_23(self, *args, **kwargs):
         if self.ativo and hasattr(self, 'projeto') and self.projeto_id:
             try:
                 tipo_projeto = Projeto.objects.get(pk=self.projeto_id).tipo
                 if tipo_projeto == Projeto.TipoPesquisa.INICIACAO_CIENTIFICA:
                     if Assessor.objects.filter(projeto_id=self.projeto_id, ativo=True).exclude(pk=self.pk).exists():
                         raise ValidationError("Projetos de Iniciação Científica só podem ter um assessor ativo por vez.")
             except Projeto.DoesNotExist:
                 pass
         super().save(*args, )
    
    xǁAssessorǁsave__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAssessorǁsave__mutmut_1': xǁAssessorǁsave__mutmut_1, 
        'xǁAssessorǁsave__mutmut_2': xǁAssessorǁsave__mutmut_2, 
        'xǁAssessorǁsave__mutmut_3': xǁAssessorǁsave__mutmut_3, 
        'xǁAssessorǁsave__mutmut_4': xǁAssessorǁsave__mutmut_4, 
        'xǁAssessorǁsave__mutmut_5': xǁAssessorǁsave__mutmut_5, 
        'xǁAssessorǁsave__mutmut_6': xǁAssessorǁsave__mutmut_6, 
        'xǁAssessorǁsave__mutmut_7': xǁAssessorǁsave__mutmut_7, 
        'xǁAssessorǁsave__mutmut_8': xǁAssessorǁsave__mutmut_8, 
        'xǁAssessorǁsave__mutmut_9': xǁAssessorǁsave__mutmut_9, 
        'xǁAssessorǁsave__mutmut_10': xǁAssessorǁsave__mutmut_10, 
        'xǁAssessorǁsave__mutmut_11': xǁAssessorǁsave__mutmut_11, 
        'xǁAssessorǁsave__mutmut_12': xǁAssessorǁsave__mutmut_12, 
        'xǁAssessorǁsave__mutmut_13': xǁAssessorǁsave__mutmut_13, 
        'xǁAssessorǁsave__mutmut_14': xǁAssessorǁsave__mutmut_14, 
        'xǁAssessorǁsave__mutmut_15': xǁAssessorǁsave__mutmut_15, 
        'xǁAssessorǁsave__mutmut_16': xǁAssessorǁsave__mutmut_16, 
        'xǁAssessorǁsave__mutmut_17': xǁAssessorǁsave__mutmut_17, 
        'xǁAssessorǁsave__mutmut_18': xǁAssessorǁsave__mutmut_18, 
        'xǁAssessorǁsave__mutmut_19': xǁAssessorǁsave__mutmut_19, 
        'xǁAssessorǁsave__mutmut_20': xǁAssessorǁsave__mutmut_20, 
        'xǁAssessorǁsave__mutmut_21': xǁAssessorǁsave__mutmut_21, 
        'xǁAssessorǁsave__mutmut_22': xǁAssessorǁsave__mutmut_22, 
        'xǁAssessorǁsave__mutmut_23': xǁAssessorǁsave__mutmut_23
    }
    
    def save(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAssessorǁsave__mutmut_orig"), object.__getattribute__(self, "xǁAssessorǁsave__mutmut_mutants"), args, kwargs, self)
        return result 
    
    save.__signature__ = _mutmut_signature(xǁAssessorǁsave__mutmut_orig)
    xǁAssessorǁsave__mutmut_orig.__name__ = 'xǁAssessorǁsave'

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
    def xǁHistAlunoǁ__str____mutmut_orig(self):
        status = "Aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_1(self):
        status = None
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_2(self):
        status = "XXAprovadoXX" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_3(self):
        status = "aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_4(self):
        status = "APROVADO" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_5(self):
        status = "Aprovado" if self.aprovado else "XXReprovadoXX"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_6(self):
        status = "Aprovado" if self.aprovado else "reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_7(self):
        status = "Aprovado" if self.aprovado else "REPROVADO"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "Aluno Desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_8(self):
        status = "Aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = None
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_9(self):
        status = "Aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "XXAluno DesconhecidoXX"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_10(self):
        status = "Aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "aluno desconhecido"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    def xǁHistAlunoǁ__str____mutmut_11(self):
        status = "Aprovado" if self.aprovado else "Reprovado"
        # Adiciona verificação se aluno existe antes de acessar o nome
        aluno_nome = self.aluno.nome if self.aluno else "ALUNO DESCONHECIDO"
        return f"Histórico de {aluno_nome} - {self.cod_disciplina} ({status})"
    
    xǁHistAlunoǁ__str____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHistAlunoǁ__str____mutmut_1': xǁHistAlunoǁ__str____mutmut_1, 
        'xǁHistAlunoǁ__str____mutmut_2': xǁHistAlunoǁ__str____mutmut_2, 
        'xǁHistAlunoǁ__str____mutmut_3': xǁHistAlunoǁ__str____mutmut_3, 
        'xǁHistAlunoǁ__str____mutmut_4': xǁHistAlunoǁ__str____mutmut_4, 
        'xǁHistAlunoǁ__str____mutmut_5': xǁHistAlunoǁ__str____mutmut_5, 
        'xǁHistAlunoǁ__str____mutmut_6': xǁHistAlunoǁ__str____mutmut_6, 
        'xǁHistAlunoǁ__str____mutmut_7': xǁHistAlunoǁ__str____mutmut_7, 
        'xǁHistAlunoǁ__str____mutmut_8': xǁHistAlunoǁ__str____mutmut_8, 
        'xǁHistAlunoǁ__str____mutmut_9': xǁHistAlunoǁ__str____mutmut_9, 
        'xǁHistAlunoǁ__str____mutmut_10': xǁHistAlunoǁ__str____mutmut_10, 
        'xǁHistAlunoǁ__str____mutmut_11': xǁHistAlunoǁ__str____mutmut_11
    }
    
    def __str__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHistAlunoǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁHistAlunoǁ__str____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __str__.__signature__ = _mutmut_signature(xǁHistAlunoǁ__str____mutmut_orig)
    xǁHistAlunoǁ__str____mutmut_orig.__name__ = 'xǁHistAlunoǁ__str__'