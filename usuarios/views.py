from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
# Aqui importamos todos os modelos que criamos no models.py
from .models import CadastroGeral, GrupoConexao, FormularioAvulso, GcLancamentoSemanal, IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala, FilaNotificacaoPush, ConfiguracaoSistema
# E aqui os serializadores
from .serializers import CadastroGeralSerializer, UsuarioSerializer, GrupoConexaoSerializer, FormularioAvulsoSerializer, GcLancamentoSemanalSerializer, ConfiguracaoSistemaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    IdeModuloSerializer, IdeFormularioSerializer, IdeTurmaSerializer,
    IdeInscricaoSerializer, IdeSalaSerializer, FilaNotificacaoPushSerializer
)

Usuario = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    """
    Retorna os dados do usuário logado para o contexto do React.
    """
    user = request.user
    dados = {
        "id": user.id,
        "login": user.email,
        "nome": user.nome,
        "celular": user.celular,
        "perfis": user.perfis,
        "acessos": user.acessos,
        "modulos": user.modulos,
        "adminModulos": user.admin_modulos,
        "liderModulos": user.lider_modulos,
        "exigeTrocaSenha": user.exige_troca_senha,
        "isGlobalAdmin": user.is_superuser 
    }
    return Response(dados)


class CadastroGeralViewSet(viewsets.ModelViewSet):
    queryset = CadastroGeral.objects.all().order_by('-dataCadastro')
    serializer_class = CadastroGeralSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome', 'celular', 'email', 'bairro', 'lider']
    permission_classes = [AllowAny] 

class FormularioAvulsoViewSet(viewsets.ModelViewSet):
    queryset = FormularioAvulso.objects.all().order_by('-dataCriacao')
    serializer_class = FormularioAvulsoSerializer
    permission_classes = [AllowAny]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('nome')
    serializer_class = UsuarioSerializer


class GrupoConexaoViewSet(viewsets.ModelViewSet):
    queryset = GrupoConexao.objects.all().order_by('lider')
    serializer_class = GrupoConexaoSerializer

class GcLancamentoSemanalViewSet(viewsets.ModelViewSet):
    queryset = GcLancamentoSemanal.objects.all().order_by('-dataGc')
    serializer_class = GcLancamentoSemanalSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['lider', 'bairro', 'usuarioResponsavel']

class ConfiguracaoSistemaViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'chave'

class IdeModuloViewSet(viewsets.ModelViewSet):
    queryset = IdeModulo.objects.all().order_by('nome')
    serializer_class = IdeModuloSerializer
    permission_classes = [AllowAny]

class IdeFormularioViewSet(viewsets.ModelViewSet):
    queryset = IdeFormulario.objects.all().order_by('-dataCriacao')
    serializer_class = IdeFormularioSerializer
    permission_classes = [AllowAny]

class IdeTurmaViewSet(viewsets.ModelViewSet):
    queryset = IdeTurma.objects.all().order_by('nome')
    serializer_class = IdeTurmaSerializer
    permission_classes = [AllowAny]

class IdeInscricaoViewSet(viewsets.ModelViewSet):
    queryset = IdeInscricao.objects.all().order_by('-dataInscricao')
    serializer_class = IdeInscricaoSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['alunoNome', 'moduloNome', 'celular']

class IdeSalaViewSet(viewsets.ModelViewSet):
    queryset = IdeSala.objects.all().order_by('-data')
    serializer_class = IdeSalaSerializer
    permission_classes = [AllowAny]

class FilaNotificacaoPushViewSet(viewsets.ModelViewSet):
    queryset = FilaNotificacaoPush.objects.all().order_by('-dataDisparo')
    serializer_class = FilaNotificacaoPushSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    modulo = request.GET.get('modulo', '').lower()
    
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    cards = []

    if modulo == 'gc':
        total_gcs = GrupoConexao.objects.count()
        gcs_homens = GrupoConexao.objects.filter(generoGc='Masculino').count()
        gcs_mulheres = GrupoConexao.objects.filter(generoGc='Feminino').count()
        
        relatorios_semana = GcLancamentoSemanal.objects.filter(
            dataGc__range=[inicio_semana, fim_semana]
        ).count()
        
        membros_gc = CadastroGeral.objects.exclude(gc__isnull=True).exclude(gc__exact='').exclude(gc__exact='Sem GC')
        total_membros = membros_gc.count()
        membros_h = membros_gc.filter(sexo='Masculino').count()
        membros_m = membros_gc.filter(sexo='Feminino').count()
        
        media = round(total_membros / total_gcs, 1) if total_gcs > 0 else 0
        
        cards = [
            {'label': 'GCs Ativos', 'valor': total_gcs, 'icone': 'Users', 'cor': 'text-[#1D14B3]'},
            {'label': 'Relatórios (Semana)', 'valor': relatorios_semana, 'icone': 'FileText', 'cor': 'text-green-500'},
            {'label': 'Perfil dos GCs', 'valor': f'{gcs_homens} H / {gcs_mulheres} M', 'icone': 'LayoutDashboard', 'cor': 'text-purple-500'},
            {'label': 'Média por GC', 'valor': media, 'icone': 'Activity', 'cor': 'text-amber-500'},
            {'label': 'Membros Totais', 'valor': total_membros, 'icone': 'UserPlus', 'cor': 'text-[#00A3E0]'},
            {'label': 'Perfil Membros', 'valor': f'{membros_h} H / {membros_m} M', 'icone': 'Users', 'cor': 'text-indigo-400'}
        ]

    elif modulo == 'ide':
        forms_abertos = IdeFormulario.objects.filter(status='Aberto').count()
        total_inscritos = IdeInscricao.objects.count()
        turmas_ativas = IdeTurma.objects.exclude(status='Encerrada').exclude(isEspera=True)
        total_turmas = turmas_ativas.count()
        
        total_alunos = 0
        for t in turmas_ativas:
            if isinstance(t.alunos, list):
                total_alunos += len(t.alunos)
                
        cards = [
            {'label': 'Formulários Abertos', 'valor': forms_abertos, 'icone': 'ClipboardList', 'cor': 'text-amber-500'},
            {'label': 'Total de Inscritos', 'valor': total_inscritos, 'icone': 'UserPlus', 'cor': 'text-[#1D14B3]'},
            {'label': 'Turmas Ativas', 'valor': total_turmas, 'icone': 'Presentation', 'cor': 'text-[#00A3E0]'},
            {'label': 'Alunos Matriculados', 'valor': total_alunos, 'icone': 'Users', 'cor': 'text-green-500'}
        ]

    elif modulo == 'gerenciamento':
        total_cadastros = CadastroGeral.objects.count()
        total_lideres = CadastroGeral.objects.filter(isLider='Sim').count()
        
        cards = [
            {'label': 'Total de Membros', 'valor': total_cadastros, 'icone': 'Database', 'cor': 'text-[#1D14B3]'},
            {'label': 'Líderes Formados', 'valor': total_lideres, 'icone': 'Star', 'cor': 'text-amber-500'}
        ]

    return Response({'cards': cards})