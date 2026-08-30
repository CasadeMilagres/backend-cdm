import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

def gerar_id_jornada():
    return uuid.uuid4().hex[:20]

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O E-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Criptografa a senha automaticamente
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    # Removemos o 'username' padrão do Django para usar o E-mail como login
    username = None
    email = models.EmailField(unique=True, verbose_name='E-mail de Login')
    
    nome = models.CharField(max_length=255, verbose_name='Nome Completo')
    celular = models.CharField(max_length=20, blank=True, null=True)
    
    # Hierarquia e Permissões do Sistema (JSON para armazenar listas)
    perfis = models.JSONField(default=list, blank=True, help_text="Ex: ['Coordenador', 'Supervisor']")
    acessos = models.JSONField(default=list, blank=True, help_text="Permissões específicas (Ex: IDE_TURMAS)")
    modulos = models.JSONField(default=list, blank=True, help_text="Módulos que pode acessar")
    admin_modulos = models.JSONField(default=list, blank=True, help_text="Módulos onde é Administrador")
    lider_modulos = models.JSONField(default=list, blank=True, help_text="Módulos onde é Líder")
    
    exige_troca_senha = models.BooleanField(default=False)
    
    # Relacionamento com a Base Global (Cadastros Gerais) que faremos depois
    cadastro_id_firebase = models.CharField(max_length=100, blank=True, null=True, help_text="ID legado do Firebase")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nome} ({self.email})"

class CadastroGeral(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    sexo = models.CharField(max_length=20, blank=True, null=True)
    dataNasc = models.DateField(blank=True, null=True)
    estadoCivil = models.CharField(max_length=50, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    lider = models.CharField(max_length=255, blank=True, null=True)
    gc = models.CharField(max_length=255, blank=True, null=True)
    isLider = models.CharField(max_length=10, default='Não')
    
    # Controle de Landing Pages (Formulários Avulsos)
    origemFormularioId = models.CharField(max_length=100, blank=True, null=True)
    origemFormularioNome = models.CharField(max_length=255, blank=True, null=True)
    respostasCustomizadas = models.JSONField(default=list, blank=True, null=True)
    dataCadastro = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nome

class FormularioAvulso(models.Model):
    titulo = models.CharField(max_length=255)
    bannerUrl = models.URLField(max_length=1000, blank=True, null=True)
    configuracaoCampos = models.JSONField(default=dict)
    perguntasCustomizadas = models.JSONField(default=list)
    criadoPor = models.CharField(max_length=150, blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class GrupoConexao(models.Model):
    nome = models.CharField(max_length=150)
    lider = models.CharField(max_length=150)
    coLider = models.CharField(max_length=150, blank=True, null=True)
    lider_supervisor = models.CharField(max_length=150, blank=True, null=True)
    supervisor = models.CharField(max_length=150, blank=True, null=True)
    coordenador = models.CharField(max_length=150, blank=True, null=True)
    anfitriao = models.CharField(max_length=150, blank=True, null=True)
    telefoneLider = models.CharField(max_length=50, blank=True, null=True)
    telefoneAnfitriao = models.CharField(max_length=50, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    dia_gc = models.CharField(max_length=50, blank=True, null=True)
    horario = models.CharField(max_length=50, blank=True, null=True)
    generoGc = models.CharField(max_length=50, default='Misto')
    tipoGc = models.CharField(max_length=50, default='Família')

    def __str__(self):
        return f"{self.nome} ({self.lider})"

class GcLancamentoSemanal(models.Model):
    grupoId = models.CharField(max_length=100, blank=True, null=True)
    lider = models.CharField(max_length=150)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    dataGc = models.DateField()
    horario = models.CharField(max_length=50, blank=True, null=True)
    statusGc = models.CharField(max_length=50, default='Ocorreu') # 'Ocorreu' ou 'Nao_Ocorreu'
    motivoNaoOcorreu = models.TextField(blank=True, null=True)
    membros = models.IntegerField(default=0)
    membrosPresentesIds = models.JSONField(default=list, blank=True)
    visitantes = models.IntegerField(default=0)
    oferta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacao = models.TextField(blank=True, null=True)
    teveOracaoCura = models.CharField(max_length=10, blank=True, null=True)
    qtdCurados = models.IntegerField(default=0)
    testemunhoCura = models.TextField(blank=True, null=True)
    imagemUrl = models.TextField(blank=True, null=True)
    usuarioResponsavel = models.CharField(max_length=150, blank=True, null=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)
    dataAtualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lider} - {self.dataGc}"

class ConfiguracaoSistema(models.Model):
    chave = models.CharField(max_length=100, unique=True)
    valor = models.JSONField(default=dict)

    def __str__(self):
        return self.chave

class IdeModulo(models.Model):
    nome = models.CharField(max_length=255)
    duracaoNum = models.IntegerField(default=1)
    duracaoTipo = models.CharField(max_length=50, default='Semanas')
    limiteFaltas = models.IntegerField(default=3)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# Tabela: Perguntas de Pré-Requisito do Módulo
class IdeModuloPergunta(models.Model):
    modulo = models.ForeignKey(IdeModulo, related_name='perguntas_rel', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255, verbose_name="Pergunta Exigida")

    class Meta:
        verbose_name = "Pergunta do Módulo"
        verbose_name_plural = "Perguntas do Módulo"

# Tabela: Grade Curricular (Aulas)
class IdeModuloAula(models.Model):
    modulo = models.ForeignKey(IdeModulo, related_name='aulas', on_delete=models.CASCADE)
    tema = models.CharField(max_length=255, verbose_name="Tema da Aula")

    class Meta:
        verbose_name = "Aula da Grade Curricular"
        verbose_name_plural = "Aulas da Grade Curricular"
        ordering = ['id']

class IdeFormulario(models.Model):
    moduloId = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    ciclo = models.CharField(max_length=100, blank=True, null=True)
    bannerUrl = models.URLField(max_length=1000, blank=True, null=True)
    linkWhatsapp = models.URLField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=50, default='Aberto')
    dataInicio = models.DateField(blank=True, null=True)
    horaInicio = models.CharField(max_length=20, blank=True, null=True)
    dataTermino = models.DateField(blank=True, null=True)
    horaTermino = models.CharField(max_length=20, blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# Tabela: Perguntas Customizadas do Formulário
class IdeFormularioPergunta(models.Model):
    formulario = models.ForeignKey(IdeFormulario, related_name='perguntas_rel', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255, verbose_name="Pergunta Customizada")

    class Meta:
        verbose_name = "Pergunta do Formulário"
        verbose_name_plural = "Perguntas Customizadas"

class IdeTurma(models.Model):
    nome = models.CharField(max_length=255)
    codigoUnico = models.CharField(max_length=50, blank=True, null=True)
    moduloId = models.CharField(max_length=100)
    moduloNome = models.CharField(max_length=255, blank=True, null=True)
    ciclo = models.CharField(max_length=100, blank=True, null=True)
    professor = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='Ativa')
    isEspera = models.BooleanField(default=False)
    formularioId = models.CharField(max_length=100, blank=True, null=True)
    diaInicio = models.DateField(blank=True, null=True)
    horarioInicio = models.CharField(max_length=50, blank=True, null=True)
    whatsappGrupo = models.URLField(max_length=1000, blank=True, null=True)
    alunos = models.JSONField(default=list, blank=True)
    removidos = models.JSONField(default=list, blank=True)
    abonosReprovacao = models.JSONField(default=list, blank=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataEncerramento = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.moduloNome})"

class IdeInscricao(models.Model):
    formularioId = models.CharField(max_length=100, blank=True, null=True)
    moduloId = models.CharField(max_length=100)
    moduloNome = models.CharField(max_length=255, blank=True, null=True)
    alunoId = models.CharField(max_length=100)
    alunoNome = models.CharField(max_length=255)
    celular = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    lider = models.CharField(max_length=255, blank=True, null=True)
    gc = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    dataNascimento = models.CharField(max_length=50, blank=True, null=True)
    estadoCivil = models.CharField(max_length=50, blank=True, null=True)
    respostas = models.JSONField(default=dict, blank=True)
    tipo = models.CharField(max_length=50, default='Formulário')
    dataInscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alunoNome} - {self.moduloNome}"

class IdeSala(models.Model):
    turmaId = models.CharField(max_length=100)
    turmaNome = models.CharField(max_length=255, blank=True, null=True)
    moduloId = models.CharField(max_length=100, blank=True, null=True)
    tema = models.CharField(max_length=255)
    data = models.CharField(max_length=50)
    diaSemana = models.CharField(max_length=50, blank=True, null=True)
    horarioInicio = models.CharField(max_length=50, blank=True, null=True)
    horarioFim = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, default='Agendada')
    presencas = models.JSONField(default=dict, blank=True)
    justificativas = models.JSONField(default=dict, blank=True)
    exercicioAtivo = models.BooleanField(default=False)
    exercicioPerguntas = models.JSONField(default=list, blank=True)
    notasExercicio = models.JSONField(default=dict, blank=True)
    respostasExercicio = models.JSONField(default=dict, blank=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tema} - {self.turmaNome}"

class FilaNotificacaoPush(models.Model):
    tipo = models.CharField(max_length=100, default='comunicado_ensino')
    turmaId = models.CharField(max_length=100, blank=True, null=True)
    turmaNome = models.CharField(max_length=255, blank=True, null=True)
    publicoAlvo = models.CharField(max_length=100, default='Todos')
    alunoNome = models.CharField(max_length=255, blank=True, null=True)
    alunoTelefone = models.CharField(max_length=50, blank=True, null=True)
    usuariosSelecionadosIds = models.JSONField(default=list, blank=True)
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField()
    status = models.CharField(max_length=50, default='pendente')
    sucessos = models.IntegerField(default=0)
    falhas = models.IntegerField(default=0)
    motivoErro = models.TextField(blank=True, null=True)
    dataDisparo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Ministerio(models.Model):
    nome = models.CharField(max_length=255)
    # lideres e funcoes <-- FORAM REMOVIDOS PARA VIRAREM TABELAS ABAIXO!

    class Meta:
        db_table = 'ministerios'
        
    def __str__(self):
        return self.nome

# NOVA TABELA PARA LÍDERES
class MinisterioLider(models.Model):
    ministerio = models.ForeignKey(Ministerio, related_name='lideres_rel', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, verbose_name="Nome do Líder")

    class Meta:
        verbose_name = "Líder do Ministério"
        verbose_name_plural = "Líderes"

# NOVA TABELA PARA CARGOS
class MinisterioFuncao(models.Model):
    ministerio = models.ForeignKey(Ministerio, related_name='funcoes_rel', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, verbose_name="Cargo / Função")
    voluntarios = models.JSONField(default=list, blank=True, verbose_name="IDs dos Voluntários")

    class Meta:
        verbose_name = "Cargo / Função"
        verbose_name_plural = "Cargos e Equipes"

class Voluntario(models.Model):
    cadastroId = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    liderGc = models.CharField(max_length=255, blank=True, null=True)
    # Array com os IDs dos ministérios: ["1", "5"]
    ministerios = models.JSONField(default=list, blank=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'voluntarios'

class EventoMinisterio(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        db_table = 'eventos_ministerio'

class EscalaMinisterio(models.Model):
    ministerioId = models.CharField(max_length=255)
    ministerioNome = models.CharField(max_length=255, blank=True, null=True)
    data = models.DateField()
    eventoId = models.CharField(max_length=255, blank=True, null=True)
    evento = models.CharField(max_length=255, blank=True, null=True)
    # Array de objetos: [{"voluntarioId": "1", "nome": "João", "funcao": "Teclado", "status": "Confirmado"}]
    escalados = models.JSONField(default=list, blank=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataAtualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'escalas_ministerio'

class ProdutoComercial(models.Model):
    modulo = models.CharField(max_length=50, default='cafeteria') # 'cafeteria' ou 'livraria'
    codigo = models.IntegerField(default=0)
    nome = models.CharField(max_length=255)
    codigoBarras = models.CharField(max_length=100, blank=True, null=True)
    precoCusto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precoVenda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estoque = models.IntegerField(default=0)
    imagemUrl = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comercial_produtos'

    def __str__(self):
        return f"[{self.modulo.upper()}] {self.nome}"

class ClienteComercial(models.Model):
    modulo = models.CharField(max_length=50, default='cafeteria')
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comercial_clientes'

    def __str__(self):
        return self.nome

class VendaComercial(models.Model):
    modulo = models.CharField(max_length=50, default='cafeteria')
    clienteId = models.CharField(max_length=255, default='Venda Avulsa')
    itens = models.JSONField(default=list, blank=True)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    formaPagamento = models.CharField(max_length=255, default='Dinheiro')
    pagamentosMult = models.JSONField(default=list, blank=True)
    vendedor = models.CharField(max_length=150, default='Sistema PDV')
    dataVenda = models.DateTimeField()
    dataPendenciaOriginal = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'comercial_vendas'

    def __str__(self):
        return f"Venda {self.id} - {self.modulo} - R$ {self.valorTotal}"

class PendenciaComercial(models.Model):
    modulo = models.CharField(max_length=50, default='cafeteria')
    clienteId = models.CharField(max_length=255)
    itens = models.JSONField(default=list, blank=True)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    formaPagamento = models.CharField(max_length=100, default='Fiado/Pendente')
    pagamentosMult = models.JSONField(default=list, blank=True)
    dataVenda = models.DateTimeField()
    vendedor = models.CharField(max_length=150, default='Sistema PDV')
    estoqueBaixado = models.BooleanField(default=False)

    class Meta:
        db_table = 'comercial_pendencias'

    def __str__(self):
        return f"Pendência {self.clienteId} - R$ {self.valorTotal}"

class EntradaEstoqueComercial(models.Model):
    modulo = models.CharField(max_length=50, default='cafeteria')
    produtoId = models.CharField(max_length=100)
    produtoNome = models.CharField(max_length=255)
    quantidadeAdicionada = models.IntegerField(default=1)
    usuario = models.CharField(max_length=150, default='Sistema')
    dataEntrada = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comercial_entradas_estoque'

    def __str__(self):
        return f"+{self.quantidadeAdicionada} {self.produtoNome}"

class ContaPagarComercial(models.Model):
    modulo = models.CharField(max_length=50, default='cafeteria')
    descricao = models.CharField(max_length=255)
    fornecedor = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vencimento = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Pendente') # 'Pendente' ou 'Pago'
    dataCadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comercial_contas_pagar'

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

class JornadaCadastro(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=gerar_id_jornada, editable=False)
    cadastroId = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=255)
    celular = models.CharField(max_length=50)
    etapa = models.IntegerField(default=0)
    exportado = models.BooleanField(default=False)
    cobrancaAtivada = models.BooleanField(default=False)
    cobrancaEnviosCount = models.IntegerField(default=0)
    historicoMensagens = models.JSONField(default=list, blank=True)
    cursosConcluidos = models.JSONField(default=list, blank=True)
    jornadaConcluida = models.BooleanField(default=False)
    dataConclusao = models.DateTimeField(blank=True, null=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jornada_cadastros'

    def __str__(self):
        return f"{self.nome} - Etapa {self.etapa}"

class MidiaBanner(models.Model):
    nomeEvento = models.CharField(max_length=255)
    linkAcao = models.URLField(max_length=1000, blank=True, null=True)
    dataHorario = models.CharField(max_length=255, blank=True, null=True)
    dataInicio = models.CharField(max_length=20)
    horaInicio = models.CharField(max_length=10, default='00:00')
    dataFim = models.CharField(max_length=20)
    horaFim = models.CharField(max_length=10, default='23:59')
    duracaoSegundos = models.IntegerField(default=4)
    ordem = models.IntegerField(default=99)
    imagemBase64 = models.URLField(max_length=1000)

class MidiaPregacao(models.Model):
    tipo = models.CharField(max_length=50, default='unica')
    titulo = models.CharField(max_length=255)
    pregador = models.CharField(max_length=255, blank=True, null=True)
    imagemBase64 = models.URLField(max_length=1000)
    audioUrl = models.URLField(max_length=1000, blank=True, null=True)
    mensagens = models.JSONField(default=list, blank=True)
    dataPublicacao = models.CharField(max_length=20, blank=True, null=True)
    horaPublicacao = models.CharField(max_length=10, default='00:00')
    timestampPublicacao = models.BigIntegerField(default=0)
    plays = models.IntegerField(default=0)
    dataCriacao = models.DateTimeField(auto_now_add=True)