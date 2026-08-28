import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
# Aqui importamos todos os modelos que criamos no models.py
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Sum, Count, Q
from django.core.cache import cache
from .models import JornadaCadastro, ConfiguracaoSistema
from .models import CadastroGeral, GrupoConexao, FormularioAvulso, GcLancamentoSemanal, IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala, FilaNotificacaoPush, ConfiguracaoSistema
# E aqui os serializadores
from .serializers import JornadaCadastroSerializer, ConfiguracaoSistemaSerializer
from .models import Ministerio, Voluntario, EventoMinisterio, EscalaMinisterio
from .models import (
    ProdutoComercial, ClienteComercial, VendaComercial,
    PendenciaComercial, EntradaEstoqueComercial, ContaPagarComercial
)
from .serializers import CadastroGeralSerializer, UsuarioSerializer, GrupoConexaoSerializer, FormularioAvulsoSerializer, GcLancamentoSemanalSerializer, ConfiguracaoSistemaSerializer
from .serializers import (
    ProdutoComercialSerializer, ClienteComercialSerializer, VendaComercialSerializer,
    PendenciaComercialSerializer, EntradaEstoqueComercialSerializer, ContaPagarComercialSerializer
)
from .serializers import (
    IdeModuloSerializer, IdeFormularioSerializer, IdeTurmaSerializer,
    IdeInscricaoSerializer, IdeSalaSerializer, FilaNotificacaoPushSerializer
)
from .serializers import (
    MinisterioSerializer, VoluntarioSerializer, 
    EventoMinisterioSerializer, EscalaMinisterioSerializer
)

Usuario = get_user_model()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def enviar_whatsapp_view(request):
    numero = request.data.get('number')
    texto = request.data.get('text')
    instance_name = request.data.get('instance', 'CDM_OFICIAL')

    if not numero or not texto:
        return Response({"error": "Número e texto são obrigatórios"}, status=400)

    url = f"{settings.EVOLUTION_API_URL}/message/sendText/{instance_name}"
    headers = {
        "Content-Type": "application/json",
        "apikey": settings.EVOLUTION_API_KEY
    }
    payload = {"number": numero, "text": texto}

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Valida se a Evolution API aceitou o envio (200 ou 201)
        if response.status_code in [200, 201]:
            return Response({"success": True, "data": response.json()})
        else:
            # Imprime o motivo real da rejeição no log do servidor
            print(f"❌ Erro Evolution API ({response.status_code}): {response.text}")
            return Response({"error": "Falha no envio do WhatsApp", "details": response.text}, status=response.status_code)
            
    except Exception as e:
        print(f"❌ Exceção ao conectar na Evolution API: {str(e)}")
        return Response({"error": str(e)}, status=500)

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

def dashboard_callback(request, context):
    cache_key = "cdm_dashboard_kpis"
    kpi_data = cache.get(cache_key)

    if not kpi_data:
        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        # Consultas agregadas e diretas
        total_membros = CadastroGeral.objects.count()
        total_lideres = CadastroGeral.objects.filter(isLider='Sim').count()

        jornada_stats = JornadaCadastro.objects.aggregate(
            total=Count('id'),
            p1=Count('id', filter=models.Q(etapa=1)),
            p2=Count('id', filter=models.Q(etapa=2)),
            p3=Count('id', filter=models.Q(etapa=3)),
            p4=Count('id', filter=models.Q(etapa=4)),
            formados=Count('id', filter=models.Q(jornadaConcluida=True)),
        )

        total_gcs = GrupoConexao.objects.count()
        gc_stats = GcLancamentoSemanal.objects.filter(
            dataGc__range=[inicio_semana, fim_semana]
        ).aggregate(
            ocorridos=Count('id', filter=models.Q(statusGc='Ocorreu')),
            nao_ocorridos=Count('id', filter=models.Q(statusGc='Nao_Ocorreu')),
            total_oferta=Sum('oferta'),
            total_membros=Sum('membros'),
            total_visitantes=Sum('visitantes'),
            total_curas=Sum('qtdCurados'),
        )

        vendas_mes = VendaComercial.objects.filter(
            dataVenda__month=hoje.month, dataVenda__year=hoje.year
        ).aggregate(total=Sum('valorTotal'))['total'] or 0.00

        pendencias_stats = PendenciaComercial.objects.aggregate(
            total=Sum('valorTotal'),
            qtd=Count('id')
        )

        contas_pagar = ContaPagarComercial.objects.filter(status='Pendente').aggregate(
            total=Sum('valor')
        )['total'] or 0.00

        turmas_ativas = IdeTurma.objects.filter(status='Ativa', isEspera=False).count()
        total_alunos_ide = IdeInscricao.objects.count()

        kpi_data = {
            'total_membros': total_membros,
            'total_lideres': total_lideres,
            'total_jornada': jornada_stats['total'] or 0,
            'jornada_passo_1': jornada_stats['p1'] or 0,
            'jornada_passo_2': jornada_stats['p2'] or 0,
            'jornada_passo_3': jornada_stats['p3'] or 0,
            'jornada_passo_4': jornada_stats['p4'] or 0,
            'jornada_formados': jornada_stats['formados'] or 0,
            'total_gcs': total_gcs,
            'gcs_ocorridos': gc_stats['ocorridos'] or 0,
            'gcs_nao_ocorridos': gc_stats['nao_ocorridos'] or 0,
            'total_oferta_gc': gc_stats['total_oferta'] or 0.00,
            'total_membros_gc': gc_stats['total_membros'] or 0,
            'total_visitantes_gc': gc_stats['total_visitantes'] or 0,
            'total_curas_gc': gc_stats['total_curas'] or 0,
            'faturamento_mes': vendas_mes,
            'total_pendencias_abertas': pendencias_stats['total'] or 0.00,
            'qtd_pendencias_abertas': pendencias_stats['qtd'] or 0,
            'contas_a_pagar_pendentes': contas_pagar,
            'turmas_ativas': turmas_ativas,
            'total_alunos_ide': total_alunos_ide,
        }
        # Salva o resultado em cache por 180 segundos
        cache.set(cache_key, kpi_data, timeout=180)

    context.update({'kpi': kpi_data})
    return context

class CadastroGeralViewSet(viewsets.ModelViewSet):
    queryset = CadastroGeral.objects.all().order_by('nome')
    serializer_class = CadastroGeralSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome', 'celular', 'email', 'cpf']

    # Adicione este bloco para liberar inscrições públicas
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class FormularioAvulsoViewSet(viewsets.ModelViewSet):
    queryset = FormularioAvulso.objects.all()
    serializer_class = FormularioAvulsoSerializer

    # Adicione este bloco para liberar a leitura do formulário
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


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
    lookup_field = 'chave'

    # 🔥 Libera apenas a LEITURA (GET) para as páginas públicas
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class IdeModuloViewSet(viewsets.ModelViewSet):
    queryset = IdeModulo.objects.all().order_by('nome')
    serializer_class = IdeModuloSerializer
    permission_classes = [AllowAny]

class IdeFormularioViewSet(viewsets.ModelViewSet):
    queryset = IdeFormulario.objects.all().order_by('-dataCriacao')
    serializer_class = IdeFormularioSerializer
    filter_backends = [SearchFilter]
    search_fields = ['titulo', 'ciclo']

    # Libera a leitura pública para que a Landing Page do IDE carregue os dados
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class IdeTurmaViewSet(viewsets.ModelViewSet):
    queryset = IdeTurma.objects.all().order_by('nome')
    serializer_class = IdeTurmaSerializer
    permission_classes = [AllowAny]

class IdeInscricaoViewSet(viewsets.ModelViewSet):
    queryset = IdeInscricao.objects.all().order_by('-dataInscricao')
    serializer_class = IdeInscricaoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['alunoNome', 'celular', 'email']

    # Libera a criação pública para que o visitante possa salvar sua matrícula
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

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

class MinisterioViewSet(viewsets.ModelViewSet):
    queryset = Ministerio.objects.all().order_by('nome')
    serializer_class = MinisterioSerializer
    permission_classes = [IsAuthenticated]

class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all().order_by('nome')
    serializer_class = VoluntarioSerializer
    permission_classes = [IsAuthenticated]

class EventoMinisterioViewSet(viewsets.ModelViewSet):
    queryset = EventoMinisterio.objects.all().order_by('nome')
    serializer_class = EventoMinisterioSerializer
    permission_classes = [IsAuthenticated]

class EscalaMinisterioViewSet(viewsets.ModelViewSet):
    queryset = EscalaMinisterio.objects.all().order_by('-data')
    serializer_class = EscalaMinisterioSerializer
    permission_classes = [IsAuthenticated]

class ProdutoComercialViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoComercialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ProdutoComercial.objects.all().order_by('codigo', 'nome')
        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)
        return qs

class ClienteComercialViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteComercialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ClienteComercial.objects.all().order_by('nome')
        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)
        return qs

class VendaComercialViewSet(viewsets.ModelViewSet):
    serializer_class = VendaComercialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = VendaComercial.objects.all().order_by('-dataVenda')
        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Baixa estoque de forma atômica se não for fiado
        itens = request.data.get('itens', [])
        modulo = request.data.get('modulo', 'cafeteria')

        for item in itens:
            prod_id = item.get('id')
            qtd = int(item.get('quantidade', 1))
            if prod_id:
                try:
                    prod = ProdutoComercial.objects.select_for_update().get(id=prod_id)
                    prod.estoque = max(0, prod.estoque - qtd)
                    prod.save()
                except ProdutoComercial.DoesNotExist:
                    pass

        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # Ao excluir venda normal, devolve os itens ao estoque
        venda = self.get_object()
        for item in (venda.itens or []):
            prod_id = item.get('id')
            qtd = int(item.get('quantidade', 0))
            if prod_id and qtd > 0:
                try:
                    prod = ProdutoComercial.objects.select_for_update().get(id=prod_id)
                    prod.estoque += qtd
                    prod.save()
                except ProdutoComercial.DoesNotExist:
                    pass
        return super().destroy(request, *args, **kwargs)

class PendenciaComercialViewSet(viewsets.ModelViewSet):
    serializer_class = PendenciaComercialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PendenciaComercial.objects.all().order_by('-dataVenda')
        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)
        return qs

    @action(detail=False, methods=['post'], url_path='quitar-lote')
    @transaction.atomic
    def quitar_lote(self, request):
        pendencias_ids = request.data.get('pendenciasIds', [])
        pagamentos = request.data.get('pagamentos', [])
        data_pagamento = request.data.get('dataPagamento')
        modulo = request.data.get('modulo', 'cafeteria')
        cliente_id = request.data.get('clienteId', 'Cliente')

        if not pendencias_ids:
            return Response({'error': 'Nenhuma pendência selecionada.'}, status=status.HTTP_400_BAD_REQUEST)

        pendencias = PendenciaComercial.objects.filter(id__in=pendencias_ids)
        total_pago = sum(float(p.get('valor', 0)) for p in pagamentos)

        # Baixa estoque dos itens se ainda não baixados
        for pend in pendencias:
            if not pend.estoqueBaixado:
                for item in (pend.itens or []):
                    prod_id = item.get('id')
                    qtd = int(item.get('quantidade', 1))
                    if prod_id:
                        try:
                            prod = ProdutoComercial.objects.select_for_update().get(id=prod_id)
                            prod.estoque = max(0, prod.estoque - qtd)
                            prod.save()
                        except ProdutoComercial.DoesNotExist:
                            pass

        formas_str = " + ".join([p.get('forma', '') for p in pagamentos if p.get('forma')])
        todos_itens = []
        for p in pendencias:
            todos_itens.extend(p.itens or [])

        # Cria a venda correspondente à quitação
        VendaComercial.objects.create(
            modulo=modulo,
            clienteId=cliente_id,
            itens=todos_itens,
            valorTotal=total_pago,
            formaPagamento=formas_str,
            pagamentosMult=pagamentos,
            vendedor="Sistema (Baixa Pendência)",
            dataVenda=data_pagamento,
            dataPendenciaOriginal=pendencias.first().dataVenda if pendencias.exists() else data_pagamento
        )

        pendencias.delete()
        return Response({'success': True, 'message': 'Pendências quitadas com sucesso!'})

class EntradaEstoqueComercialViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaEstoqueComercialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = EntradaEstoqueComercial.objects.all().order_by('-dataEntrada')
        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        prod_id = request.data.get('produtoId')
        qtd = int(request.data.get('quantidadeAdicionada', 0))

        if prod_id and qtd > 0:
            try:
                prod = ProdutoComercial.objects.select_for_update().get(id=prod_id)
                prod.estoque += qtd
                prod.save()
            except ProdutoComercial.DoesNotExist:
                return Response({'error': 'Produto não localizado.'}, status=status.HTTP_404_NOT_FOUND)

        return super().create(request, *args, **kwargs)

class ContaPagarComercialViewSet(viewsets.ModelViewSet):
    serializer_class = ContaPagarComercialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ContaPagarComercial.objects.all().order_by('-vencimento')
        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)
        return qs

# =======================================================
# CLASSES DE JORNADA E CONFIGURAÇÃO
# =======================================================
class JornadaCadastroViewSet(viewsets.ModelViewSet):
    queryset = JornadaCadastro.objects.all().order_by('-dataCadastro')
    serializer_class = JornadaCadastroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['etapa', 'exportado', 'jornadaConcluida']

    def get_permissions(self):
        # Validação segura da ação sem gerar AttributeError
        if getattr(self, 'action', None) in ['create', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class ConfiguracaoSistemaViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    lookup_field = 'chave'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]