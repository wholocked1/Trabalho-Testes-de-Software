# src/core/views.py

from django.db import IntegrityError
from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Imports das Camadas de Serviço e Repositório
from . import services as core_services
from . import repositories as core_repo

# Imports dos Modelos (apenas para exceções)
from .models import Professor, Aluno, Projeto, ProfessorLattes, HistAluno, Departamento

# Imports dos Serializers (Camada de Apresentação)
from .serializers import (
    ProfessorSerializer,
    AlunoSerializer,
    ProjetoSerializer,
    ProfessorLattesSerializer,
    HistAlunoSerializer,
    DepartamentoSerializer,
    ProfessorLattesKeywordsSerializer
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

class ProfessorViewSet(viewsets.ModelViewSet):
    """ ViewSet para Professores (público). """
    lookup_field = 'id_professor' # Define o nome do argumento da URL
    queryset = core_repo.get_all_professors_with_dept()
    serializer_class = ProfessorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['get'])
    # --- CORREÇÃO --- (pk=None -> id_professor=None)
    def lattes(self, request, id_professor=None):
        """ Retorna as informações do Lattes para um professor específico. """
        try:
            professor = self.get_object() # self.get_object() ainda funciona
            lattes = core_repo.get_lattes_by_professor(professor)
            serializer = ProfessorLattesSerializer(lattes)
            return Response(serializer.data)
        except ProfessorLattes.DoesNotExist:
            return Response({'error': 'Informações Lattes não encontradas.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='contagem-projetos')
    # --- CORREÇÃO --- (pk=None -> id_professor=None)
    def contagem_projetos(self, request, id_professor=None):
        """ Retorna a contagem de projetos ativos onde o professor é orientador/assessor. """
        try:
            # --- CORREÇÃO --- (Usa o argumento id_professor)
            resposta_servico = core_services.get_professor_project_counts(id_professor)
            return Response(resposta_servico)
        except ObjectDoesNotExist as e:
             return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlunoViewSet(viewsets.ModelViewSet):
    """ ViewSet para Alunos (público). """
    lookup_field = 'id_aluno' # Define o nome do argumento da URL
    queryset = core_repo.get_all_alunos_with_curso()
    serializer_class = AlunoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['get'])
    # --- CORREÇÃO --- (pk=None -> id_aluno=None)
    def historico(self, request, id_aluno=None):
        """ Retorna o histórico acadêmico para um aluno específico. """
        # --- CORREÇÃO --- (Usa o argumento id_aluno)
        historico_list = core_repo.get_historico_by_aluno_id(id_aluno)
        serializer = HistAlunoSerializer(historico_list, many=True)
        return Response(serializer.data)


class ProjetoViewSet(viewsets.ModelViewSet):
    """ ViewSet completo para Projetos (público). """
    lookup_field = 'id_proj' # Define o nome do argumento da URL
    queryset = core_repo.get_all_projects_prefetched()
    serializer_class = ProjetoSerializer

    def xǁProjetoViewSetǁget_queryset__mutmut_orig(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_1(self):
        # ... (O get_queryset não muda) ...
        queryset = None
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_2(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = None
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_3(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get(None)
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_4(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('XXorientador_idXX')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_5(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('ORIENTADOR_ID')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_6(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = None
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_7(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=None)
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_8(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(None))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_9(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = None
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_10(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get(None)
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_11(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('XXassessor_idXX')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_12(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('ASSESSOR_ID')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_13(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = None
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_14(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=None)
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_15(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(None))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_16(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = None
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_17(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get(None)
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_18(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('XXpendenciaXX')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_19(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('PENDENCIA')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_20(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = ""
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_21(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.upper() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_22(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() not in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_23(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.upper():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_24(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = None; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_25(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; return
                 if status_valor is not None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_26(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is None: queryset = queryset.filter(pendencia=status_valor)
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_27(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = None
            except: pass
        return queryset.distinct()

    def xǁProjetoViewSetǁget_queryset__mutmut_28(self):
        # ... (O get_queryset não muda) ...
        queryset = super().get_queryset()
        orientador_id = self.request.query_params.get('orientador_id')
        if orientador_id:
            try:
                queryset = queryset.filter(orientadores__id_professor=int(orientador_id))
            except ValueError: pass
        assessor_id = self.request.query_params.get('assessor_id')
        if assessor_id:
            try:
                queryset = queryset.filter(assessores__id_professor=int(assessor_id))
            except ValueError: pass
        pendencia_texto = self.request.query_params.get('pendencia')
        if pendencia_texto:
            try:
                 status_valor = None
                 for choice_val, choice_name in Projeto.StatusProjeto.choices:
                     if pendencia_texto.lower() in choice_name.lower():
                         status_valor = choice_val; break
                 if status_valor is not None: queryset = queryset.filter(pendencia=None)
            except: pass
        return queryset.distinct()
    
    xǁProjetoViewSetǁget_queryset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProjetoViewSetǁget_queryset__mutmut_1': xǁProjetoViewSetǁget_queryset__mutmut_1, 
        'xǁProjetoViewSetǁget_queryset__mutmut_2': xǁProjetoViewSetǁget_queryset__mutmut_2, 
        'xǁProjetoViewSetǁget_queryset__mutmut_3': xǁProjetoViewSetǁget_queryset__mutmut_3, 
        'xǁProjetoViewSetǁget_queryset__mutmut_4': xǁProjetoViewSetǁget_queryset__mutmut_4, 
        'xǁProjetoViewSetǁget_queryset__mutmut_5': xǁProjetoViewSetǁget_queryset__mutmut_5, 
        'xǁProjetoViewSetǁget_queryset__mutmut_6': xǁProjetoViewSetǁget_queryset__mutmut_6, 
        'xǁProjetoViewSetǁget_queryset__mutmut_7': xǁProjetoViewSetǁget_queryset__mutmut_7, 
        'xǁProjetoViewSetǁget_queryset__mutmut_8': xǁProjetoViewSetǁget_queryset__mutmut_8, 
        'xǁProjetoViewSetǁget_queryset__mutmut_9': xǁProjetoViewSetǁget_queryset__mutmut_9, 
        'xǁProjetoViewSetǁget_queryset__mutmut_10': xǁProjetoViewSetǁget_queryset__mutmut_10, 
        'xǁProjetoViewSetǁget_queryset__mutmut_11': xǁProjetoViewSetǁget_queryset__mutmut_11, 
        'xǁProjetoViewSetǁget_queryset__mutmut_12': xǁProjetoViewSetǁget_queryset__mutmut_12, 
        'xǁProjetoViewSetǁget_queryset__mutmut_13': xǁProjetoViewSetǁget_queryset__mutmut_13, 
        'xǁProjetoViewSetǁget_queryset__mutmut_14': xǁProjetoViewSetǁget_queryset__mutmut_14, 
        'xǁProjetoViewSetǁget_queryset__mutmut_15': xǁProjetoViewSetǁget_queryset__mutmut_15, 
        'xǁProjetoViewSetǁget_queryset__mutmut_16': xǁProjetoViewSetǁget_queryset__mutmut_16, 
        'xǁProjetoViewSetǁget_queryset__mutmut_17': xǁProjetoViewSetǁget_queryset__mutmut_17, 
        'xǁProjetoViewSetǁget_queryset__mutmut_18': xǁProjetoViewSetǁget_queryset__mutmut_18, 
        'xǁProjetoViewSetǁget_queryset__mutmut_19': xǁProjetoViewSetǁget_queryset__mutmut_19, 
        'xǁProjetoViewSetǁget_queryset__mutmut_20': xǁProjetoViewSetǁget_queryset__mutmut_20, 
        'xǁProjetoViewSetǁget_queryset__mutmut_21': xǁProjetoViewSetǁget_queryset__mutmut_21, 
        'xǁProjetoViewSetǁget_queryset__mutmut_22': xǁProjetoViewSetǁget_queryset__mutmut_22, 
        'xǁProjetoViewSetǁget_queryset__mutmut_23': xǁProjetoViewSetǁget_queryset__mutmut_23, 
        'xǁProjetoViewSetǁget_queryset__mutmut_24': xǁProjetoViewSetǁget_queryset__mutmut_24, 
        'xǁProjetoViewSetǁget_queryset__mutmut_25': xǁProjetoViewSetǁget_queryset__mutmut_25, 
        'xǁProjetoViewSetǁget_queryset__mutmut_26': xǁProjetoViewSetǁget_queryset__mutmut_26, 
        'xǁProjetoViewSetǁget_queryset__mutmut_27': xǁProjetoViewSetǁget_queryset__mutmut_27, 
        'xǁProjetoViewSetǁget_queryset__mutmut_28': xǁProjetoViewSetǁget_queryset__mutmut_28
    }
    
    def get_queryset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProjetoViewSetǁget_queryset__mutmut_orig"), object.__getattribute__(self, "xǁProjetoViewSetǁget_queryset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_queryset.__signature__ = _mutmut_signature(xǁProjetoViewSetǁget_queryset__mutmut_orig)
    xǁProjetoViewSetǁget_queryset__mutmut_orig.__name__ = 'xǁProjetoViewSetǁget_queryset'

    def xǁProjetoViewSetǁcreate__mutmut_orig(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_1(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = None
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_2(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(None)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_3(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = None
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_4(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_5(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(None, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_6(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=None)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_7(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_8(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, )
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_9(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = None
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_10(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(None, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_11(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, None, str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_12(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', None)
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_13(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr('message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_14(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_15(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', )
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_16(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'XXmessageXX', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_17(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'MESSAGE', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_18(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(None))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_19(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(None, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_20(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, None): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_21(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr('messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_22(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, ): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_23(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'XXmessagesXX'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_24(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'MESSAGES'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_25(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = None
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_26(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(None)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_27(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "XX; XX".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_28(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response(None, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_29(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=None)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_30(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_31(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, )
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_32(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'XXerrorXX': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_33(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'ERROR': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_34(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_35(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=None)

    def xǁProjetoViewSetǁcreate__mutmut_36(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_37(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, )

    def xǁProjetoViewSetǁcreate__mutmut_38(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'XXerrorXX': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_39(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'ERROR': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def xǁProjetoViewSetǁcreate__mutmut_40(self, request, *args, **kwargs):
        # ... (O create não muda) ...
        try:
            projeto = core_services.create_project_with_associations(request.data)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(None)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    xǁProjetoViewSetǁcreate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProjetoViewSetǁcreate__mutmut_1': xǁProjetoViewSetǁcreate__mutmut_1, 
        'xǁProjetoViewSetǁcreate__mutmut_2': xǁProjetoViewSetǁcreate__mutmut_2, 
        'xǁProjetoViewSetǁcreate__mutmut_3': xǁProjetoViewSetǁcreate__mutmut_3, 
        'xǁProjetoViewSetǁcreate__mutmut_4': xǁProjetoViewSetǁcreate__mutmut_4, 
        'xǁProjetoViewSetǁcreate__mutmut_5': xǁProjetoViewSetǁcreate__mutmut_5, 
        'xǁProjetoViewSetǁcreate__mutmut_6': xǁProjetoViewSetǁcreate__mutmut_6, 
        'xǁProjetoViewSetǁcreate__mutmut_7': xǁProjetoViewSetǁcreate__mutmut_7, 
        'xǁProjetoViewSetǁcreate__mutmut_8': xǁProjetoViewSetǁcreate__mutmut_8, 
        'xǁProjetoViewSetǁcreate__mutmut_9': xǁProjetoViewSetǁcreate__mutmut_9, 
        'xǁProjetoViewSetǁcreate__mutmut_10': xǁProjetoViewSetǁcreate__mutmut_10, 
        'xǁProjetoViewSetǁcreate__mutmut_11': xǁProjetoViewSetǁcreate__mutmut_11, 
        'xǁProjetoViewSetǁcreate__mutmut_12': xǁProjetoViewSetǁcreate__mutmut_12, 
        'xǁProjetoViewSetǁcreate__mutmut_13': xǁProjetoViewSetǁcreate__mutmut_13, 
        'xǁProjetoViewSetǁcreate__mutmut_14': xǁProjetoViewSetǁcreate__mutmut_14, 
        'xǁProjetoViewSetǁcreate__mutmut_15': xǁProjetoViewSetǁcreate__mutmut_15, 
        'xǁProjetoViewSetǁcreate__mutmut_16': xǁProjetoViewSetǁcreate__mutmut_16, 
        'xǁProjetoViewSetǁcreate__mutmut_17': xǁProjetoViewSetǁcreate__mutmut_17, 
        'xǁProjetoViewSetǁcreate__mutmut_18': xǁProjetoViewSetǁcreate__mutmut_18, 
        'xǁProjetoViewSetǁcreate__mutmut_19': xǁProjetoViewSetǁcreate__mutmut_19, 
        'xǁProjetoViewSetǁcreate__mutmut_20': xǁProjetoViewSetǁcreate__mutmut_20, 
        'xǁProjetoViewSetǁcreate__mutmut_21': xǁProjetoViewSetǁcreate__mutmut_21, 
        'xǁProjetoViewSetǁcreate__mutmut_22': xǁProjetoViewSetǁcreate__mutmut_22, 
        'xǁProjetoViewSetǁcreate__mutmut_23': xǁProjetoViewSetǁcreate__mutmut_23, 
        'xǁProjetoViewSetǁcreate__mutmut_24': xǁProjetoViewSetǁcreate__mutmut_24, 
        'xǁProjetoViewSetǁcreate__mutmut_25': xǁProjetoViewSetǁcreate__mutmut_25, 
        'xǁProjetoViewSetǁcreate__mutmut_26': xǁProjetoViewSetǁcreate__mutmut_26, 
        'xǁProjetoViewSetǁcreate__mutmut_27': xǁProjetoViewSetǁcreate__mutmut_27, 
        'xǁProjetoViewSetǁcreate__mutmut_28': xǁProjetoViewSetǁcreate__mutmut_28, 
        'xǁProjetoViewSetǁcreate__mutmut_29': xǁProjetoViewSetǁcreate__mutmut_29, 
        'xǁProjetoViewSetǁcreate__mutmut_30': xǁProjetoViewSetǁcreate__mutmut_30, 
        'xǁProjetoViewSetǁcreate__mutmut_31': xǁProjetoViewSetǁcreate__mutmut_31, 
        'xǁProjetoViewSetǁcreate__mutmut_32': xǁProjetoViewSetǁcreate__mutmut_32, 
        'xǁProjetoViewSetǁcreate__mutmut_33': xǁProjetoViewSetǁcreate__mutmut_33, 
        'xǁProjetoViewSetǁcreate__mutmut_34': xǁProjetoViewSetǁcreate__mutmut_34, 
        'xǁProjetoViewSetǁcreate__mutmut_35': xǁProjetoViewSetǁcreate__mutmut_35, 
        'xǁProjetoViewSetǁcreate__mutmut_36': xǁProjetoViewSetǁcreate__mutmut_36, 
        'xǁProjetoViewSetǁcreate__mutmut_37': xǁProjetoViewSetǁcreate__mutmut_37, 
        'xǁProjetoViewSetǁcreate__mutmut_38': xǁProjetoViewSetǁcreate__mutmut_38, 
        'xǁProjetoViewSetǁcreate__mutmut_39': xǁProjetoViewSetǁcreate__mutmut_39, 
        'xǁProjetoViewSetǁcreate__mutmut_40': xǁProjetoViewSetǁcreate__mutmut_40
    }
    
    def create(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProjetoViewSetǁcreate__mutmut_orig"), object.__getattribute__(self, "xǁProjetoViewSetǁcreate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create.__signature__ = _mutmut_signature(xǁProjetoViewSetǁcreate__mutmut_orig)
    xǁProjetoViewSetǁcreate__mutmut_orig.__name__ = 'xǁProjetoViewSetǁcreate'

    @action(detail=True, methods=['post'], url_path='associar-aluno')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def associar_aluno(self, request, id_proj=None):
        """ Associa um aluno a um projeto existente. """
        aluno_id = request.data.get('id_aluno')
        if not aluno_id: return Response({'error': '"id_aluno" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # --- CORREÇÃO --- (Usa o argumento id_proj)
            core_services.associate_aluno_to_project(id_proj, aluno_id)
            return Response({'status': 'Aluno associado.'})
        except (ValidationError, ObjectDoesNotExist) as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='associar-assessor')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def associar_assessor(self, request, id_proj=None):
        """ Associa um professor como assessor a um projeto existente. """
        assessor_id = request.data.get('id_professor')
        if not assessor_id: return Response({'error': '"id_professor" (assessor) obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # --- CORREÇÃO --- (Usa o argumento id_proj)
            core_services.associate_assessor_to_project(id_proj, assessor_id)
            return Response({'status': 'Assessor associado.'})
        except (ValidationError, ObjectDoesNotExist) as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='link-mongo')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def link_mongo(self, request, id_proj=None):
        """ Associa um ID do MongoDB a um projeto. """
        mongo_id_str = request.data.get('mongo_id')
        try:
            # --- CORREÇÃO --- (Usa o argumento id_proj)
            projeto = core_services.link_mongo_to_project(id_proj, mongo_id_str)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data)
        except (ValidationError, ObjectDoesNotExist) as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='orientador-departamento')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def orientador_departamento(self, request, id_proj=None):
        """ Retorna o ID do departamento do primeiro orientador associado ao projeto. """
        try:
            projeto = self.get_object() # self.get_object() usa o 'lookup_field', então não precisa do id_proj
            dept = core_repo.get_first_orientador_departamento(projeto)
            return Response({'id_departamento_orientador': dept.id_departamento})
        except ObjectDoesNotExist as e: 
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='associar-orientador')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def associar_orientador(self, request, id_proj=None):
        """ Associa um professor como orientador a um projeto existente. """
        orientador_id = request.data.get('id_professor')
        if not orientador_id: return Response({'error': '"id_professor" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # --- CORREÇÃO --- (Usa o argumento id_proj)
            core_services.associate_orientador_to_project(id_proj, orientador_id)
            return Response({'status': 'Orientador associado.'})
        except (ValidationError, ObjectDoesNotExist) as e:
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ObjectDoesNotExist) else status.HTTP_400_BAD_REQUEST
            return Response({'error': str(e)}, status=status_code)

    @action(detail=True, methods=['post'], url_path='desativar-participante')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def desativar_participante(self, request, id_proj=None):
        """ Define o status 'ativo' como False para o ÚNICO participante ATIVO de um 'role'. """
        role = request.data.get('role')
        try:
            # --- CORREÇÃO --- (Usa o argumento id_proj)
            status_message = core_services.deactivate_project_participant(id_proj, role)
            return Response({'status': status_message})
        except (ValidationError, ObjectDoesNotExist) as e:
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ObjectDoesNotExist) else status.HTTP_400_BAD_REQUEST
            return Response({'error': str(e)}, status=status_code)
        except Exception as e: 
            return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='salvar-corretor')
    # --- CORREÇÃO --- (pk=None -> id_proj=None)
    def salvar_corretor(self, request, id_proj=None):
        """ Salva o texto do 'melhor_corretor' no projeto. """
        texto_corretor = request.data.get('texto_corretor')
        try:
            # --- CORREÇÃO --- (Usa o argumento id_proj)
            projeto = core_services.save_corretor_text(id_proj, texto_corretor)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data)
        except (ValidationError, ObjectDoesNotExist) as e:
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ObjectDoesNotExist) else status.HTTP_400_BAD_REQUEST
            return Response({'error': str(e)}, status=status_code)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao salvar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet apenas para leitura de Departamentos. """
    lookup_field = 'id_departamento' # Define o nome do argumento da URL
    queryset = core_repo.get_all_departments()
    serializer_class = DepartamentoSerializer

    @action(detail=True, methods=['get'], url_path='professores-keywords')
    # --- CORREÇÃO --- (pk=None -> id_departamento=None)
    def professores_keywords(self, request, id_departamento=None):
        """ Retorna ID e keywords Lattes dos professores deste departamento. """
        # --- CORREÇÃO --- (Usa o argumento id_departamento)
        lattes = core_repo.get_lattes_keywords_by_dept_id(id_departamento)
        serializer = ProfessorLattesKeywordsSerializer(lattes, many=True)
        return Response(serializer.data)

class AllProfessorLattesKeywordsView(generics.ListAPIView):
    """ Retorna uma lista contendo ID e keywords Lattes de TODOS os professores. """
    queryset = core_repo.get_all_lattes_keywords()
    serializer_class = ProfessorLattesKeywordsSerializer

class ProfessorLattesViewSet(viewsets.ModelViewSet):
    """ ViewSet para gerenciar as informações do Lattes dos professores. """
    queryset = core_repo.get_all_lattes()
    serializer_class = ProfessorLattesSerializer
    lookup_field = 'professor' # Este já estava correto