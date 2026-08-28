from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

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
    perguntas = models.JSONField(default=list, blank=True)
    limiteFaltas = models.IntegerField(default=3)
    gradeCurricular = models.JSONField(default=list, blank=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

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
    perguntas = models.JSONField(default=list, blank=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

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
    # Guarda o array de nomes dos líderes: ["João", "Maria"]
    lideres = models.JSONField(default=list, blank=True)
    # Guarda o array de objetos das funções: [{"id": "xyz", "nome": "Baterista", "voluntarios": ["id1", "id2"]}]
    funcoes = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'ministerios'

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