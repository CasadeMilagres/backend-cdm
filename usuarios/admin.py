from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import (
    Usuario, CadastroGeral, FormularioAvulso, GrupoConexao, GcLancamentoSemanal,
    ConfiguracaoSistema, IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala,
    FilaNotificacaoPush, Ministerio, Voluntario, EventoMinisterio, EscalaMinisterio,
    ProdutoComercial, ClienteComercial, VendaComercial, PendenciaComercial,
    EntradaEstoqueComercial, ContaPagarComercial, JornadaCadastro,
    IdeModuloAula, MinisterioLider, MinisterioFuncao, IdeModuloPergunta, IdeFormularioPergunta # Novas tabelas
)

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin, ModelAdmin):
    ordering = ('email',)
    list_display = ('nome_formatado', 'email_formatado', 'mostrar_perfis', 'mostrar_modulos', 'status_staff', 'status_superuser')
    search_fields = ('nome', 'email', 'celular')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        ("Credenciais", {"fields": ("email", "password")}),
        ("Dados Pessoais", {"fields": ("nome", "celular")}),
        ("Permissões & Módulos", {"fields": ("perfis", "modulos", "admin_modulos", "lider_modulos", "acessos", "exige_troca_senha")}),
        ("Acesso Django", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password'),
        }),
    )

    @display(description="Nome Completo")
    def nome_formatado(self, obj):
        nome_tratado = (obj.nome or "Sem Nome").title()
        return format_html("<span class='text-gray-900 dark:text-gray-200'>{}</span>", nome_tratado)

    @display(description="E-mail de Login")
    def email_formatado(self, obj):
        return format_html("<span class='text-xs text-gray-500 dark:text-gray-400'>{}</span>", obj.email or "-")

    @display(description="Perfis")
    def mostrar_perfis(self, obj):
        if not obj.perfis:
            return mark_safe("<span class='cdm-status-inactive'>—</span>")
        badges = [f"<span class='cdm-badge cdm-badge-blue'>{p}</span>" for p in obj.perfis]
        return mark_safe(f"<div class='flex flex-wrap gap-1'>{''.join(badges)}</div>")

    @display(description="Módulos Liberados")
    def mostrar_modulos(self, obj):
        if not obj.modulos:
            return mark_safe("<span class='cdm-status-inactive'>—</span>")
        badges = [f"<span class='cdm-badge cdm-badge-cyan'>{str(m).upper()}</span>" for m in obj.modulos]
        return mark_safe(f"<div class='flex flex-wrap gap-1'>{''.join(badges)}</div>")

    @display(description="Staff")
    def status_staff(self, obj):
        if obj.is_staff:
            return mark_safe("<span class='cdm-badge cdm-badge-emerald'>Staff</span>")
        return mark_safe("<span class='cdm-status-inactive'>—</span>")

    @display(description="Admin Geral")
    def status_superuser(self, obj):
        if obj.is_superuser:
            return mark_safe("<span class='cdm-badge cdm-badge-purple'>Superuser</span>")
        return mark_safe("<span class='cdm-status-inactive'>—</span>")

@admin.register(CadastroGeral)
class CadastroGeralAdmin(ModelAdmin):
    list_display = ('nome_formatado', 'celular', 'bairro', 'lider', 'gc', 'tag_lider', 'dataCadastro')
    search_fields = ('nome', 'celular', 'email', 'cpf', 'bairro')
    list_filter = ('isLider', 'sexo', 'estadoCivil', 'bairro')

    @display(description="Nome")
    def nome_formatado(self, obj):
        return format_html("<span class='text-gray-900 dark:text-gray-200'>{}</span>", (obj.nome or "").title())

    @display(description="Liderança")
    def tag_lider(self, obj):
        if obj.isLider == 'Sim':
            return mark_safe("<span class='cdm-badge cdm-badge-emerald'>Líder</span>")
        return mark_safe("<span class='cdm-status-inactive'>Membro</span>")

@admin.register(JornadaCadastro)
class JornadaCadastroAdmin(ModelAdmin):
    list_display = ('nome_formatado', 'celular', 'tag_etapa', 'status_conclusao', 'dataCadastro')
    search_fields = ('nome', 'celular')
    list_filter = ('etapa', 'jornadaConcluida', 'exportado', 'cobrancaAtivada')

    @display(description="Nome")
    def nome_formatado(self, obj):
        return format_html("<span class='text-gray-900 dark:text-gray-200'>{}</span>", (obj.nome or "").title())

    @display(description="Etapa da Jornada")
    def tag_etapa(self, obj):
        mapa = {
            0: ("cdm-badge-muted", "Decisão Inicial"),
            1: ("cdm-badge-blue", "Passo 1 • Bem-vindo"),
            2: ("cdm-badge-cyan", "Passo 2 • Inserção GC"),
            3: ("cdm-badge-purple", "Passo 3 • Ministérios"),
            4: ("cdm-badge-amber", "Passo 4 • Ensino IDE"),
            5: ("cdm-badge-emerald", "Formado 🎉"),
        }
        classe, nome = mapa.get(obj.etapa, ("cdm-badge-muted", f"Passo {obj.etapa}"))
        return mark_safe(f"<span class='cdm-badge {classe}'>{nome}</span>")

    @display(description="Conclusão")
    def status_conclusao(self, obj):
        if obj.jornadaConcluida:
            return mark_safe("<span class='cdm-badge cdm-badge-emerald'>Concluído</span>")
        return mark_safe("<span class='cdm-status-inactive'>Em Trilha</span>")

@admin.register(GrupoConexao)
class GrupoConexaoAdmin(ModelAdmin):
    list_display = ('nome', 'lider', 'coordenador', 'bairro', 'dia_gc', 'horario')
    search_fields = ('nome', 'lider', 'coordenador', 'bairro')
    list_filter = ('dia_gc', 'generoGc', 'tipoGc', 'bairro')

@admin.register(GcLancamentoSemanal)
class GcLancamentoSemanalAdmin(ModelAdmin):
    list_display = ('lider', 'bairro', 'dataGc', 'tag_status', 'membros', 'visitantes', 'valor_oferta', 'qtdCurados')
    search_fields = ('lider', 'bairro', 'observacao')
    list_filter = ('statusGc', 'teveOracaoCura', 'dataGc')

    @display(description="Status GC")
    def tag_status(self, obj):
        if obj.statusGc == 'Ocorreu':
            return mark_safe("<span class='cdm-badge cdm-badge-emerald'>Realizado</span>")
        return mark_safe("<span class='cdm-badge cdm-badge-amber'>Não Ocorreu</span>")

    @display(description="Oferta")
    def valor_oferta(self, obj):
        return f"R$ {obj.oferta:.2f}"

@admin.register(IdeTurma)
class IdeTurmaAdmin(ModelAdmin):
    list_display = ('nome', 'moduloNome', 'professor', 'ciclo', 'tag_status', 'qtd_alunos')
    search_fields = ('nome', 'professor', 'moduloNome')
    list_filter = ('status', 'isEspera', 'moduloNome')

    @display(description="Status")
    def tag_status(self, obj):
        if obj.status == 'Ativa':
            return mark_safe("<span class='cdm-badge cdm-badge-emerald'>Ativa</span>")
        return mark_safe("<span class='cdm-badge cdm-badge-muted'>Encerrada</span>")

    @display(description="Alunos")
    def qtd_alunos(self, obj):
        return len(obj.alunos) if isinstance(obj.alunos, list) else 0

# --- INLINES DO MÓDULO IDE ---
class IdeModuloPerguntaInline(TabularInline):
    model = IdeModuloPergunta
    extra = 1

class IdeModuloAulaInline(TabularInline):
    model = IdeModuloAula
    extra = 1

@admin.register(IdeModulo)
class IdeModuloAdmin(ModelAdmin):
    list_display = ('nome', 'duracaoNum', 'duracaoTipo', 'limiteFaltas')
    search_fields = ('nome',)
    inlines = [IdeModuloPerguntaInline, IdeModuloAulaInline] # Grade Curricular e Perguntas Editáveis!

# --- INLINES DO FORMULÁRIO IDE ---
class IdeFormularioPerguntaInline(TabularInline):
    model = IdeFormularioPergunta
    extra = 1

# --- INSCRIÇÕES (Agrupadas por Módulo) ---
@admin.register(IdeInscricao)
class IdeInscricaoAdmin(ModelAdmin):
    # Organiza a exibição: Módulo > Aluno
    list_display = ('moduloNome', 'alunoNome', 'celular', 'lider', 'dataInscricao')
    list_display_links = ('alunoNome',)
    search_fields = ('alunoNome', 'celular', 'lider')
    # O list_filter cria um menu lateral lindo no Unfold para você clicar no Curso e ver só os alunos dele
    list_filter = ('moduloNome', 'dataInscricao', 'tipo')
    ordering = ('moduloNome', 'alunoNome')

# --- SALAS DE AULA (Agrupadas por Turma) ---
@admin.register(IdeSala)
class IdeSalaAdmin(ModelAdmin):
    # Organiza a exibição: Turma > Aula
    list_display = ('turmaNome', 'tema', 'data', 'horarioInicio', 'status')
    list_display_links = ('tema',)
    search_fields = ('tema', 'turmaNome')
    # Filtro lateral por turma
    list_filter = ('turmaNome', 'status')
    ordering = ('turmaNome', '-data')

# --- INLINES E ADMIN DE MINISTÉRIOS ---
class MinisterioLiderInline(TabularInline):
    model = MinisterioLider
    extra = 1

class MinisterioFuncaoInline(TabularInline):
    model = MinisterioFuncao
    extra = 1
    fields = ('nome',) 

@admin.register(Ministerio)
class MinisterioAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [MinisterioLiderInline, MinisterioFuncaoInline]

@admin.register(Voluntario)
class VoluntarioAdmin(ModelAdmin):
    list_display = ('nome', 'telefone', 'sexo', 'liderGc', 'qtd_ministerios')
    search_fields = ('nome', 'telefone', 'liderGc')
    list_filter = ('sexo',)

    @display(description="Vínculos")
    def qtd_ministerios(self, obj):
        return f"{len(obj.ministerios)} ministérios" if isinstance(obj.ministerios, list) else "0"

@admin.register(EscalaMinisterio)
class EscalaMinisterioAdmin(ModelAdmin):
    list_display = ('evento', 'ministerioNome', 'data', 'qtd_escalados')
    search_fields = ('evento', 'ministerioNome')
    list_filter = ('ministerioNome', 'data')

    @display(description="Escalados")
    def qtd_escalados(self, obj):
        return len(obj.escalados) if isinstance(obj.escalados, list) else 0

@admin.register(ProdutoComercial)
class ProdutoComercialAdmin(ModelAdmin):
    list_display = ('nome', 'modulo', 'codigo', 'estoque', 'preco_custo_fmt', 'preco_venda_fmt')
    search_fields = ('nome', 'codigoBarras')
    list_filter = ('modulo', 'categoria')

    @display(description="Custo")
    def preco_custo_fmt(self, obj):
        return f"R$ {obj.precoCusto:.2f}"

    @display(description="Venda")
    def preco_venda_fmt(self, obj):
        return f"R$ {obj.precoVenda:.2f}"

@admin.register(VendaComercial)
class VendaComercialAdmin(ModelAdmin):
    list_display = ('clienteId', 'modulo', 'valor_total_fmt', 'formaPagamento', 'dataVenda')
    search_fields = ('clienteId', 'formaPagamento')
    list_filter = ('modulo', 'formaPagamento', 'dataVenda')

    @display(description="Total")
    def valor_total_fmt(self, obj):
        return f"R$ {obj.valorTotal:.2f}"

@admin.register(PendenciaComercial)
class PendenciaComercialAdmin(ModelAdmin):
    list_display = ('clienteId', 'modulo', 'valor_total_fmt', 'formaPagamento', 'dataVenda')
    search_fields = ('clienteId',)
    list_filter = ('modulo', 'dataVenda')

    @display(description="Valor em Aberto")
    def valor_total_fmt(self, obj):
        return f"R$ {obj.valorTotal:.2f}"

@admin.register(ContaPagarComercial)
class ContaPagarComercialAdmin(ModelAdmin):
    list_display = ('descricao', 'modulo', 'fornecedor', 'valor_fmt', 'vencimento', 'tag_status')
    search_fields = ('descricao', 'fornecedor')
    list_filter = ('modulo', 'status', 'vencimento')

    @display(description="Valor")
    def valor_fmt(self, obj):
        return f"R$ {obj.valor:.2f}"

    @display(description="Status")
    def tag_status(self, obj):
        if obj.status == 'Pago':
            return mark_safe("<span class='cdm-badge cdm-badge-emerald'>Pago</span>")
        return mark_safe("<span class='cdm-badge cdm-badge-amber'>Pendente</span>")

@admin.register(ClienteComercial)
class ClienteComercialAdmin(ModelAdmin):
    list_display = ('nome', 'modulo', 'telefone', 'email')
    search_fields = ('nome', 'telefone')

@admin.register(EntradaEstoqueComercial)
class EntradaEstoqueComercialAdmin(ModelAdmin):
    list_display = ('produtoNome', 'modulo', 'quantidadeAdicionada', 'dataEntrada')
    search_fields = ('produtoNome',)

@admin.register(FilaNotificacaoPush)
class FilaNotificacaoPushAdmin(ModelAdmin):
    list_display = ('titulo', 'tipo', 'publicoAlvo', 'status', 'dataDisparo')
    search_fields = ('titulo', 'alunoNome')

@admin.register(FormularioAvulso)
class FormularioAvulsoAdmin(ModelAdmin):
    list_display = ('titulo', 'criadoPor', 'dataCriacao')

@admin.register(IdeFormulario)
class IdeFormularioAdmin(ModelAdmin):
    list_display = ('titulo', 'status', 'ciclo')
    list_filter = ('status', 'ciclo')
    inlines = [IdeFormularioPerguntaInline] # Perguntas editáveis no Admin!

@admin.register(EventoMinisterio)
class EventoMinisterioAdmin(ModelAdmin):
    list_display = ('nome',)

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(ModelAdmin):
    list_display = ('chave',)