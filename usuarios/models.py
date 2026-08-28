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
    codigo = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=150)
    lider = models.CharField(max_length=150)
    lider_supervisor = models.CharField(max_length=150, blank=True, null=True)
    supervisor = models.CharField(max_length=150, blank=True, null=True)
    coordenador = models.CharField(max_length=150, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    dia_gc = models.CharField(max_length=50, blank=True, null=True)
    horario = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome