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
    FormularioAvulsoViewSet # Novo
)

# Roteador automatico do Django para CRUD completo (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r'cadastros', CadastroGeralViewSet, basename='cadastros')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'grupos', GrupoConexaoViewSet, basename='grupos')
router.register(r'formularios_avulsos', FormularioAvulsoViewSet, basename='formularios_avulsos') # Novo

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', perfil_usuario, name='perfil_usuario'),
    
    # Adiciona as rotas de cadastros, usuarios e grupos
    path('api/', include(router.urls)),
]