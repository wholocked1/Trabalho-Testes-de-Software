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

    def get_queryset(self):
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

    def create(self, request, *args, **kwargs):
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