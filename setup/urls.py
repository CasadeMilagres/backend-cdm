from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# Importação corrigida com todas as views
from usuarios.views import (
    perfil_usuario, 
    CadastroGeralViewSet, 
    UsuarioViewSet, 
    GrupoConexaoViewSet,
    FormularioAvulsoViewSet,
    IdeModuloViewSet, IdeFormularioViewSet, IdeTurmaViewSet,
    IdeInscricaoViewSet, IdeSalaViewSet, FilaNotificacaoPushViewSet # Novo
)

# Roteador automatico do Django para CRUD completo (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r'cadastros', CadastroGeralViewSet, basename='cadastros')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'grupos', GrupoConexaoViewSet, basename='grupos')
router.register(r'formularios_avulsos', FormularioAvulsoViewSet, basename='formularios_avulsos')
router.register(r'ide_modulos', IdeModuloViewSet, basename='ide_modulos')
router.register(r'ide_formularios', IdeFormularioViewSet, basename='ide_formularios')
router.register(r'ide_turmas', IdeTurmaViewSet, basename='ide_turmas')
router.register(r'ide_inscricoes', IdeInscricaoViewSet, basename='ide_inscricoes')
router.register(r'ide_salas', IdeSalaViewSet, basename='ide_salas')
router.register(r'fila_notificacoes_push', FilaNotificacaoPushViewSet, basename='fila_notificacoes_push')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', perfil_usuario, name='perfil_usuario'),
    
    # Adiciona as rotas de cadastros, usuarios e grupos
    path('api/', include(router.urls)),
]