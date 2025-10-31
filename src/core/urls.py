# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfessorViewSet,
    AlunoViewSet,
    ProjetoViewSet,
    DepartamentoViewSet,
    AllProfessorLattesKeywordsView,
    ProfessorLattesViewSet
)

router = DefaultRouter()
router.register(r'professores', ProfessorViewSet, basename='professor')
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'projetos', ProjetoViewSet, basename='projeto')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'lattes', ProfessorLattesViewSet, basename='lattes')

urlpatterns = [
    # Inclui /api/professores/, /api/alunos/, /api/projetos/, etc.
    path('', include(router.urls)), 
    
    # --- URL ALTERADA AQUI ---
    # Agora é um endpoint de nível superior
    path('lattes-keywords/', AllProfessorLattesKeywordsView.as_view(), name='all-lattes-keywords'),
]