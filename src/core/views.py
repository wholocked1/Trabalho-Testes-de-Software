# core/views.py

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
    # ProfessorCreateSerializer, # Agora usado apenas no service
    ProfessorLattesSerializer,
    HistAlunoSerializer,
    DepartamentoSerializer,
    ProfessorLattesKeywordsSerializer
)

class ProfessorViewSet(viewsets.ModelViewSet):
    """ ViewSet para Professores (público). """
    # Chama o REPOSITÓRIO para buscar dados
    queryset = core_repo.get_all_professors_with_dept()
    serializer_class = ProfessorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['get'])
    def lattes(self, request, pk=None):
        """ Retorna as informações do Lattes para um professor específico. """
        try:
            professor = self.get_object() # self.get_object() ainda é ok de usar
            # Chama o REPOSITÓRIO
            lattes = core_repo.get_lattes_by_professor(professor)
            serializer = ProfessorLattesSerializer(lattes)
            return Response(serializer.data)
        except ProfessorLattes.DoesNotExist:
            return Response({'error': 'Informações Lattes não encontradas.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='contagem-projetos')
    def contagem_projetos(self, request, pk=None):
        """ Retorna a contagem de projetos ativos onde o professor é orientador/assessor. """
        try:
            # Chama o SERVIÇO para executar a lógica de negócio
            resposta_servico = core_services.get_professor_project_counts(pk)
            return Response(resposta_servico)
        except ObjectDoesNotExist as e:
             return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Tratamento de exceção genérico [cite: 44]
            return Response({'error': f'Ocorreu um erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlunoViewSet(viewsets.ModelViewSet):
    """ ViewSet para Alunos (público). """
    # Chama o REPOSITÓRIO
    queryset = core_repo.get_all_alunos_with_curso()
    serializer_class = AlunoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """ Retorna o histórico acadêmico para um aluno específico. """
        # Chama o REPOSITÓRIO
        historico_list = core_repo.get_historico_by_aluno_id(pk)
        serializer = HistAlunoSerializer(historico_list, many=True)
        return Response(serializer.data)


class ProjetoViewSet(viewsets.ModelViewSet):
    """ ViewSet completo para Projetos (público). """
    # Chama o REPOSITÓRIO
    queryset = core_repo.get_all_projects_prefetched()
    serializer_class = ProjetoSerializer

    def get_queryset(self):
        """ Filtra a lista de projetos (lógica de filtro pode ficar na view). """
        queryset = super().get_queryset()
        # ... (seu código de filtro existente está OK aqui, 
        #    ou pode ser movido para o repositório se ficar muito complexo)
        # ...
        return queryset.distinct()

    def create(self, request, *args, **kwargs):
        """ Cria um novo projeto e associa orientador/aluno se fornecidos. """
        try:
            # Chama o SERVIÇO para executar a criação
            projeto = core_services.create_project_with_associations(request.data)
            
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Trata exceções personalizadas vindas do serviço [cite: 44]
        except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
             msg = getattr(e, 'message', str(e))
             if hasattr(e, 'messages'): msg = "; ".join(e.messages)
             return Response({'error': f'Erro: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='associar-aluno')
    def associar_aluno(self, request, pk=None):
        """ Associa um aluno a um projeto existente. """
        aluno_id = request.data.get('id_aluno')
        if not aluno_id: return Response({'error': '"id_aluno" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Chama o SERVIÇO
            core_services.associate_aluno_to_project(pk, aluno_id)
            return Response({'status': 'Aluno associado.'})
        except (ValidationError, ObjectDoesNotExist) as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='associar-assessor')
    def associar_assessor(self, request, pk=None):
        """ Associa um professor como assessor a um projeto existente. """
        assessor_id = request.data.get('id_professor')
        if not assessor_id: return Response({'error': '"id_professor" (assessor) obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Chama o SERVIÇO
            core_services.associate_assessor_to_project(pk, assessor_id)
            return Response({'status': 'Assessor associado.'})
        except (ValidationError, ObjectDoesNotExist) as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='link-mongo')
    def link_mongo(self, request, pk=None):
        """ Associa um ID do MongoDB a um projeto. """
        mongo_id_str = request.data.get('mongo_id')
        try:
            # Chama o SERVIÇO
            projeto = core_services.link_mongo_to_project(pk, mongo_id_str)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data)
        except (ValidationError, ObjectDoesNotExist) as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='orientador-departamento')
    def orientador_departamento(self, request, pk=None):
        """ Retorna o ID do departamento do primeiro orientador associado ao projeto. """
        try:
            projeto = self.get_object()
            # Chama o REPOSITÓRIO
            dept = core_repo.get_first_orientador_departamento(projeto)
            return Response({'id_departamento_orientador': dept.id_departamento})
        except ObjectDoesNotExist as e: 
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='associar-orientador')
    def associar_orientador(self, request, pk=None):
        """ Associa um professor como orientador a um projeto existente. """
        orientador_id = request.data.get('id_professor')
        if not orientador_id: return Response({'error': '"id_professor" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Chama o SERVIÇO
            core_services.associate_orientador_to_project(pk, orientador_id)
            return Response({'status': 'Orientador associado.'})
        except (ValidationError, ObjectDoesNotExist) as e:
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ObjectDoesNotExist) else status.HTTP_400_BAD_REQUEST
            return Response({'error': str(e)}, status=status_code)

    @action(detail=True, methods=['post'], url_path='desativar-participante')
    def desativar_participante(self, request, pk=None):
        """ Define o status 'ativo' como False para o ÚNICO participante ATIVO de um 'role'. """
        role = request.data.get('role')
        try:
            # Chama o SERVIÇO
            status_message = core_services.deactivate_project_participant(pk, role)
            return Response({'status': status_message})
        except (ValidationError, ObjectDoesNotExist) as e:
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ObjectDoesNotExist) else status.HTTP_400_BAD_REQUEST
            return Response({'error': str(e)}, status=status_code)
        except Exception as e: 
            return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='salvar-corretor')
    def salvar_corretor(self, request, pk=None):
        """ Salva o texto do 'melhor_corretor' no projeto. """
        texto_corretor = request.data.get('texto_corretor')
        try:
            # Chama o SERVIÇO
            projeto = core_services.save_corretor_text(pk, texto_corretor)
            serializer = self.get_serializer(projeto)
            return Response(serializer.data)
        except (ValidationError, ObjectDoesNotExist) as e:
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ObjectDoesNotExist) else status.HTTP_400_BAD_REQUEST
            return Response({'error': str(e)}, status=status_code)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao salvar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet apenas para leitura de Departamentos. """
    # Chama o REPOSITÓRIO
    queryset = core_repo.get_all_departments()
    serializer_class = DepartamentoSerializer

    @action(detail=True, methods=['get'], url_path='professores-keywords')
    def professores_keywords(self, request, pk=None):
        """ Retorna ID e keywords Lattes dos professores deste departamento. """
        # Chama o REPOSITÓRIO
        lattes = core_repo.get_lattes_keywords_by_dept_id(pk)
        serializer = ProfessorLattesKeywordsSerializer(lattes, many=True)
        return Response(serializer.data)

class AllProfessorLattesKeywordsView(generics.ListAPIView):
    """ Retorna uma lista contendo ID e keywords Lattes de TODOS os professores. """
    # Chama o REPOSITÓRIO
    queryset = core_repo.get_all_lattes_keywords()
    serializer_class = ProfessorLattesKeywordsSerializer

class ProfessorLattesViewSet(viewsets.ModelViewSet):
    """ ViewSet para gerenciar as informações do Lattes dos professores. """
    # Chama o REPOSITÓRY
    queryset = core_repo.get_all_lattes()
    serializer_class = ProfessorLattesSerializer
    lookup_field = 'professor'