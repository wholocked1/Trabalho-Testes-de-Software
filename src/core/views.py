# core/views.py

from django.db import transaction, IntegrityError
from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

# Imports dos Modelos
from .models import (
    Professor,
    Aluno,
    Projeto,
    Orientador,
    AlunoProj,
    Assessor,
    ProfessorLattes,
    HistAluno,
    Departamento
)
# Imports dos Serializers
from .serializers import (
    ProfessorSerializer,
    AlunoSerializer,
    ProjetoSerializer,
    ProfessorCreateSerializer,
    ProfessorLattesSerializer,
    HistAlunoSerializer,
    DepartamentoSerializer,
    ProfessorLattesKeywordsSerializer
)

class ProfessorViewSet(viewsets.ModelViewSet):
    """ ViewSet para Professores (público). """
    queryset = Professor.objects.all().select_related('departamento')
    serializer_class = ProfessorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['get'])
    def lattes(self, request, pk=None):
        """ Retorna as informações do Lattes para um professor específico. """
        professor = self.get_object()
        try:
            lattes = professor.professorlattes
            serializer = ProfessorLattesSerializer(lattes)
            return Response(serializer.data)
        except ProfessorLattes.DoesNotExist:
            return Response({'error': 'Informações Lattes não encontradas para este professor.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='contagem-projetos')
    def contagem_projetos(self, request, pk=None):
        """ Retorna a contagem de projetos ativos onde o professor é orientador/assessor. """
        try:
            professor = self.get_object()
            contagem_orientador_ativo = professor.orientador_set.filter(ativo=True).count()
            contagem_assessor_ativo = professor.assessor_set.filter(ativo=True).count()
            resposta = {
                'id_professor': professor.id_professor,
                'nome_professor': professor.nome,
                'orientacoes_ativas': contagem_orientador_ativo,
                'assessorias_ativas': contagem_assessor_ativo
            }
            return Response(resposta)
        except Professor.DoesNotExist:
             return Response({'error': 'Professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlunoViewSet(viewsets.ModelViewSet):
    """ ViewSet para Alunos (público). """
    queryset = Aluno.objects.all().select_related('curso')
    serializer_class = AlunoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """ Retorna o histórico acadêmico para um aluno específico. """
        historico_list = HistAluno.objects.filter(aluno__id_aluno=pk)
        serializer = HistAlunoSerializer(historico_list, many=True)
        return Response(serializer.data)


class ProjetoViewSet(viewsets.ModelViewSet):
    """ ViewSet completo para Projetos (público). """
    queryset = Projeto.objects.all().prefetch_related(
        'alunoproj_set__aluno', 'orientador_set__professor', 'assessor_set__professor'
    )
    serializer_class = ProjetoSerializer

    def get_queryset(self):
        """ Filtra a lista de projetos baseado em parâmetros de query. """
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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Cria um novo projeto e associa orientador/aluno se fornecidos. """
        dados = request.data
        orientador_id_input = dados.get('id_professor')
        orientador_novo_dados = dados.get('orientador_novo')
        aluno_id_input = dados.get('id_aluno')

        orientador_obj_criado = None
        orientador_id_final = None
        aluno_obj_encontrado = None
        aluno_id_final = None

        try:
            if orientador_novo_dados:
                prof_serializer = ProfessorCreateSerializer(data=orientador_novo_dados)
                prof_serializer.is_valid(raise_exception=True)
                orientador_obj_criado = prof_serializer.save()
                orientador_id_final = orientador_obj_criado.id_professor
            elif orientador_id_input:
                orientador_obj_criado = Professor.objects.get(id_professor=orientador_id_input)
                orientador_id_final = orientador_id_input

            if aluno_id_input:
                aluno_obj_encontrado = Aluno.objects.get(id_aluno=aluno_id_input)
                aluno_id_final = aluno_id_input

            projeto = Projeto.objects.create(
                tema=dados.get('tema'), tipo=dados.get('tipo'),
                resumo=dados.get('resumo'), palavra_chave=dados.get('palavra_chave', ''),
                duracao=dados.get('duracao'), bolsa=dados.get('bolsa'),
            )

            if orientador_obj_criado:
                Orientador.objects.create(professor=orientador_obj_criado, projeto=projeto)
            if aluno_obj_encontrado:
                AlunoProj.objects.create(aluno=aluno_obj_encontrado, projeto=projeto)

            projeto.refresh_from_db()
            serializer = self.get_serializer(projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Professor.DoesNotExist:
            return Response({'error': f'Professor orientador com ID {orientador_id_input} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Aluno.DoesNotExist:
             return Response({'error': f'Aluno com ID {aluno_id_input} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
             return Response({'error': f'Erro de integridade: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
             msg = e.messages[0] if hasattr(e, 'messages') else str(e)
             return Response({'error': f'Erro de validação: {msg}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='associar-aluno')
    def associar_aluno(self, request, pk=None):
        """ Associa um aluno a um projeto existente. """
        projeto = self.get_object()
        aluno_id = request.data.get('id_aluno')
        if not aluno_id: return Response({'error': '"id_aluno" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            AlunoProj.objects.create(aluno_id=aluno_id, projeto=projeto)
            return Response({'status': 'Aluno associado.'})
        except ValidationError as e: return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='associar-assessor')
    def associar_assessor(self, request, pk=None):
        """ Associa um professor como assessor a um projeto existente. """
        projeto = self.get_object()
        assessor_id = request.data.get('id_professor')
        if not assessor_id: return Response({'error': '"id_professor" (assessor) obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if projeto.orientadores.filter(id_professor=assessor_id).exists():
                return Response({'error': 'Orientador não pode ser assessor.'}, status=status.HTTP_400_BAD_REQUEST)
            Assessor.objects.create(professor_id=assessor_id, projeto=projeto)
            return Response({'status': 'Assessor associado.'})
        except ValidationError as e: return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='link-mongo')
    def link_mongo(self, request, pk=None):
        """ Associa um ID do MongoDB a um projeto. """
        projeto = self.get_object()
        mongo_id_str = request.data.get('mongo_id')
        if not mongo_id_str or len(mongo_id_str) != 24: return Response({'error': '"mongo_id" inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            projeto.mongo_id = mongo_id_str
            projeto.save(); serializer = self.get_serializer(projeto); return Response(serializer.data)
        except Exception as e: return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='orientador-departamento')
    def orientador_departamento(self, request, pk=None):
        """ Retorna o ID do departamento do primeiro orientador associado ao projeto. """
        try:
            projeto = self.get_object(); orientador_rel = projeto.orientador_set.order_by('-ativo').first()
            if not orientador_rel: return Response({'error': 'Nenhum orientador.'}, status=status.HTTP_404_NOT_FOUND)
            dept = orientador_rel.professor.departamento
            if not dept: return Response({'error': 'Orientador sem depto.'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'id_departamento_orientador': dept.id_departamento})
        except Projeto.DoesNotExist: return Response({'error': 'Projeto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='associar-orientador')
    def associar_orientador(self, request, pk=None):
        """ Associa um professor como orientador a um projeto existente, SOMENTE se não houver um orientador ativo. """
        projeto = self.get_object(); orientador_id = request.data.get('id_professor')
        if not orientador_id: return Response({'error': '"id_professor" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Orientador.objects.create(professor_id=orientador_id, projeto=projeto)
            return Response({'status': 'Orientador associado.'})
        except Professor.DoesNotExist: return Response({'error': f'Professor {orientador_id} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e: return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='desativar-participante')
    def desativar_participante(self, request, pk=None):
        """ Define o status 'ativo' como False para o ÚNICO participante ATIVO de um 'role'. """
        projeto = self.get_object(); role = request.data.get('role')
        if not role: return Response({'error': '"role" obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        if role not in ['aluno', 'orientador', 'assessor']: return Response({'error': 'Role inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target_model = None; related_queryset = None
            if role == 'aluno': target_model = AlunoProj; related_queryset = projeto.alunoproj_set
            elif role == 'orientador': target_model = Orientador; related_queryset = projeto.orientador_set
            elif role == 'assessor': target_model = Assessor; related_queryset = projeto.assessor_set
            rel_ativos = related_queryset.filter(ativo=True); contagem = rel_ativos.count()
            if contagem == 0: return Response({'error': f'Nenhum {role} ativo.'}, status=status.HTTP_404_NOT_FOUND)
            elif contagem > 1: return Response({'error': f'Múltiplos {role}s ativos.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                rel = rel_ativos.get(); rel.ativo = False; rel.save()
                return Response({'status': f'Status do {role} atualizado para inativo.'})
        except Exception as e: return Response({'error': f'Erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # --- NOVA FUNÇÃO ADICIONADA AQUI ---
    @action(detail=True, methods=['post'], url_path='salvar-corretor')
    def salvar_corretor(self, request, pk=None):
        """
        Recebe um texto e o salva no campo 'melhor_corretor' do projeto.
        'pk' aqui é o id_proj.
        """
        projeto = self.get_object()
        texto_corretor = request.data.get('texto_corretor')

        if texto_corretor is None:
            return Response(
                {'error': 'O campo "texto_corretor" é obrigatório no corpo da requisição.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            projeto.melhor_corretor = texto_corretor
            projeto.save()
            serializer = self.get_serializer(projeto)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro ao salvar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet apenas para leitura de Departamentos. """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

    @action(detail=True, methods=['get'], url_path='professores-keywords')
    def professores_keywords(self, request, pk=None):
        """ Retorna ID e keywords Lattes dos professores deste departamento. """
        lattes = ProfessorLattes.objects.select_related('professor').filter(professor__departamento_id=pk)
        serializer = ProfessorLattesKeywordsSerializer(lattes, many=True); return Response(serializer.data)

class AllProfessorLattesKeywordsView(generics.ListAPIView):
    """ Retorna uma lista contendo ID e keywords Lattes de TODOS os professores. """
    queryset = ProfessorLattes.objects.select_related('professor').all(); serializer_class = ProfessorLattesKeywordsSerializer

class ProfessorLattesViewSet(viewsets.ModelViewSet):
    """ ViewSet para gerenciar as informações do Lattes dos professores. """
    queryset = ProfessorLattes.objects.all(); serializer_class = ProfessorLattesSerializer; lookup_field = 'professor'

# As views de Login, Logout e CurrentUser foram REMOVIDAS.