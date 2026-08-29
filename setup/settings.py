import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-insegura-apenas-para-dev')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    # 🔥 Unfold deve ser o primeiro
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'django_filters',
    'corsheaders',
    'usuarios',
]

UNFOLD = {
    "SITE_TITLE": "Casa de Milagres",
    "SITE_HEADER": "Casa de Milagres",
    "SITE_URL": "/admin/",
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "165 180 252",
            "400": "0 163 224",    # Ciano CDM (#00A3E0)
            "500": "29 20 179",    # Azul Moderno CDM (#1D14B3)
            "600": "24 16 150",
            "700": "20 14 122",
            "800": "16 12 99",
            "900": "10 8 66",
            "950": "6 5 45",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Membresia & Liderança",
                "separator": True,
                "items": [
                    {
                        "title": "Base Global de Pessoas",
                        "icon": "person",
                        "link": lambda r: reverse_lazy("admin:usuarios_cadastrogeral_changelist"),
                    },
                    {
                        "title": "Usuários do Sistema",
                        "icon": "group",
                        "link": lambda r: reverse_lazy("admin:usuarios_usuario_changelist"),
                    },
                    {
                        "title": "Jornada do Membro",
                        "icon": "timeline",
                        "link": lambda r: reverse_lazy("admin:usuarios_jornadacadastro_changelist"),
                    },
                    {
                        "title": "Landing Pages Avulsas",
                        "icon": "web",
                        "link": lambda r: reverse_lazy("admin:usuarios_formularioavulso_changelist"),
                    },
                ],
            },
            {
                "title": "Células / Grupos de Conexão",
                "separator": True,
                "items": [
                    {
                        "title": "Grupos de Conexão (GCs)",
                        "icon": "hub",
                        "link": lambda r: reverse_lazy("admin:usuarios_grupoconexao_changelist"),
                    },
                    {
                        "title": "Lançamentos Semanais",
                        "icon": "event_available",
                        "link": lambda r: reverse_lazy("admin:usuarios_gclancamentosemanal_changelist"),
                    },
                ],
            },
            {
                "title": "Ensino (IDE)",
                "separator": True,
                "items": [
                    {
                        "title": "Cursos / Módulos",
                        "icon": "school",
                        "link": lambda r: reverse_lazy("admin:usuarios_idemodulo_changelist"),
                    },
                    {
                        "title": "Turmas Ativas",
                        "icon": "groups",
                        "link": lambda r: reverse_lazy("admin:usuarios_ideturma_changelist"),
                    },
                    {
                        "title": "Inscrições nos Cursos",
                        "icon": "how_to_reg",
                        "link": lambda r: reverse_lazy("admin:usuarios_ideinscricao_changelist"),
                    },
                    {
                        "title": "Diário de Aulas / Presenças",
                        "icon": "assignment",
                        "link": lambda r: reverse_lazy("admin:usuarios_idesala_changelist"),
                    },
                    {
                        "title": "Formulários de Matrícula",
                        "icon": "feed",
                        "link": lambda r: reverse_lazy("admin:usuarios_ideformulario_changelist"),
                    },
                ],
            },
            {
                "title": "Operação Ministerial",
                "separator": True,
                "items": [
                    {
                        "title": "Ministérios",
                        "icon": "volunteer_activism",
                        "link": lambda r: reverse_lazy("admin:usuarios_ministerio_changelist"),
                    },
                    {
                        "title": "Voluntários Registrados",
                        "icon": "assignment_ind",
                        "link": lambda r: reverse_lazy("admin:usuarios_voluntario_changelist"),
                    },
                    {
                        "title": "Escalas & Eventos",
                        "icon": "event_note",
                        "link": lambda r: reverse_lazy("admin:usuarios_escalaministerio_changelist"),
                    },
                ],
            },
            {
                "title": "Comercial & Financeiro",
                "separator": True,
                "items": [
                    {
                        "title": "Produtos / Livraria & Café",
                        "icon": "inventory_2",
                        "link": lambda r: reverse_lazy("admin:usuarios_produtocomercial_changelist"),
                    },
                    {
                        "title": "Vendas Concluídas",
                        "icon": "point_of_sale",
                        "link": lambda r: reverse_lazy("admin:usuarios_vendacomercial_changelist"),
                    },
                    {
                        "title": "Contas Pendentes (Fiados)",
                        "icon": "pending_actions",
                        "link": lambda r: reverse_lazy("admin:usuarios_pendenciacomercial_changelist"),
                    },
                    {
                        "title": "Contas a Pagar",
                        "icon": "request_quote",
                        "link": lambda r: reverse_lazy("admin:usuarios_contapagarcomercial_changelist"),
                    },
                    {
                        "title": "Entradas de Estoque",
                        "icon": "move_to_inbox",
                        "link": lambda r: reverse_lazy("admin:usuarios_entradaestoquecomercial_changelist"),
                    },
                ],
            },
            {
                "title": "Sistema & Comunicação",
                "separator": True,
                "items": [
                    {
                        "title": "Fila de Mensagens / WhatsApp",
                        "icon": "chat",
                        "link": lambda r: reverse_lazy("admin:usuarios_filanotificacaopush_changelist"),
                    },
                    {
                        "title": "Configurações Globais",
                        "icon": "settings",
                        "link": lambda r: reverse_lazy("admin:usuarios_configuracaosistema_changelist"),
                    },
                ],
            },
        ],
    },
}

# Certifique-se de configurar STATICFILES_DIRS se ainda não tiver:
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Mantida apenas uma ocorrência
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Configurações da Evolution API (também no .env)
EVOLUTION_API_URL = os.environ.get('EVOLUTION_API_URL', 'https://whatsapp.casademilagres.com')
EVOLUTION_API_KEY = os.environ.get('EVOLUTION_API_KEY', '')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

AUTH_USER_MODEL = 'usuarios.Usuario'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False

# Permite que o Django entenda o HTTPS do Cloud Run
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://backend-cdm-api-934434685854.us-central1.run.app',
    'https://*.run.app',
]