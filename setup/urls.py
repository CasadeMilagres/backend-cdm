from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usuarios.views import (
    perfil_usuario,
    dashboard_stats,
    CadastroGeralViewSet,
    UsuarioViewSet,
    GrupoConexaoViewSet,
    FormularioAvulsoViewSet,
    IdeModuloViewSet,
    IdeFormularioViewSet,
    IdeTurmaViewSet,
    IdeInscricaoViewSet,
    IdeSalaViewSet,
    FilaNotificacaoPushViewSet,
    GcLancamentoSemanalViewSet,
    ConfiguracaoSistemaViewSet,
    MinisterioViewSet, 
    VoluntarioViewSet, 
    EventoMinisterioViewSet, 
    EscalaMinisterioViewSet,
    ProdutoComercialViewSet,
    ClienteComercialViewSet,
    VendaComercialViewSet,
    PendenciaComercialViewSet,
    EntradaEstoqueComercialViewSet,
    ContaPagarComercialViewSet,
    JornadaCadastroViewSet, 
    ConfiguracaoSistemaViewSet
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
router.register(r'gc_lancamentos', GcLancamentoSemanalViewSet, basename='gc_lancamentos')
router.register(r'configuracoes', ConfiguracaoSistemaViewSet, basename='configuracoes')
router.register(r'ministerios', MinisterioViewSet, basename='ministerio')
router.register(r'voluntarios', VoluntarioViewSet, basename='voluntario')
router.register(r'eventos_ministerio', EventoMinisterioViewSet, basename='eventos_ministerio')
router.register(r'escalas_ministerio', EscalaMinisterioViewSet, basename='escalas_ministerio')
router.register(r'comercial/produtos', ProdutoComercialViewSet, basename='comercial-produtos')
router.register(r'comercial/clientes', ClienteComercialViewSet, basename='comercial-clientes')
router.register(r'comercial/vendas', VendaComercialViewSet, basename='comercial-vendas')
router.register(r'comercial/pendencias', PendenciaComercialViewSet, basename='comercial-pendencias')
router.register(r'comercial/entradas-estoque', EntradaEstoqueComercialViewSet, basename='comercial-entradas')
router.register(r'comercial/contas-pagar', ContaPagarComercialViewSet, basename='comercial-contas-pagar')
router.register(r'jornada', JornadaCadastroViewSet, basename='jornada')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/perfil/', perfil_usuario, name='perfil_usuario'),
    path('api/dashboard/', dashboard_stats, name='dashboard_stats'),
    path('api/', include(router.urls)),
]