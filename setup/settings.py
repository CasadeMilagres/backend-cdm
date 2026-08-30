import os
import firebase_admin
from firebase_admin import credentials
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.templatetags.static import static

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

FIREBASE_KEY_PATH = os.path.join(BASE_DIR, 'firebase-key.json')
if os.path.exists(FIREBASE_KEY_PATH) and not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'casa-de-milagres-d6193.firebasestorage.app'
    })

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
    "SITE_LOGO": {
        "light": lambda request: static("img/logo-completa.png"),
        "dark": lambda request: static("img/logo-completa.png"),
    },
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "STYLES": [
        lambda request: static("css/custom.css"),
    ],
    "COLORS": {
        "primary": {
            "50": "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "0 163 224",
            "400": "0 130 200",
            "500": "29 20 179",
            "600": "24 16 150",
            "700": "20 14 122",
            "800": "16 12 99",
            "900": "10 10 12",
            "950": "5 5 7",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Visão Geral",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard Principal",
                        "icon": "dashboard",
                        "link": lambda r: reverse_lazy("admin:index"),
                    },
                ],
            },
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
                        "title": "Líderes de GC Registrados",
                        "icon": "star",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_cadastrogeral_changelist')}?isLider__exact=Sim",
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
                ],
            },
            {
                "title": "Grupos de Conexão (GCs)",
                "separator": True,
                "items": [
                    {
                        "title": "Gerenciar GCs",
                        "icon": "hub",
                        "link": lambda r: reverse_lazy("admin:usuarios_grupoconexao_changelist"),
                    },
                    {
                        "title": "Lançamento Semanal (Novo)",
                        "icon": "add_task",
                        "link": lambda r: reverse_lazy("admin:usuarios_gclancamentosemanal_add"),
                    },
                    {
                        "title": "Consulta de Lançamentos",
                        "icon": "find_in_page",
                        "link": lambda r: reverse_lazy("admin:usuarios_gclancamentosemanal_changelist"),
                    },
                    {
                        "title": "Formulários & Configurações",
                        "icon": "rule",
                        "link": lambda r: reverse_lazy("admin:usuarios_formularioavulso_changelist"),
                    },
                ],
            },
            {
                "title": "Ensino (IDE)",
                "separator": True,
                "items": [
                    {
                        "title": "Cursos & Módulos",
                        "icon": "auto_stories",
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
                        "title": "Sala de Aula / Presenças",
                        "icon": "co_present",
                        "link": lambda r: reverse_lazy("admin:usuarios_idesala_changelist"),
                    },
                    {
                        "title": "Formulários de Matrícula",
                        "icon": "feed",
                        "link": lambda r: reverse_lazy("admin:usuarios_ideformulario_changelist"),
                    },
                    {
                        "title": "Comunicação & Pushes",
                        "icon": "campaign",
                        "link": lambda r: reverse_lazy("admin:usuarios_filanotificacaopush_changelist"),
                    },
                ],
            },
            {
                "title": "Cafeteria CDM",
                "separator": True,
                "items": [
                    {
                        "title": "Produtos da Cafeteria",
                        "icon": "local_cafe",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_produtocomercial_changelist')}?modulo__exact=cafeteria",
                    },
                    {
                        "title": "Vendas Realizadas",
                        "icon": "point_of_sale",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_vendacomercial_changelist')}?modulo__exact=cafeteria",
                    },
                    {
                        "title": "Contas Pendentes (Fiados)",
                        "icon": "pending_actions",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_pendenciacomercial_changelist')}?modulo__exact=cafeteria",
                    },
                ],
            },
            {
                "title": "Livraria CDM",
                "separator": True,
                "items": [
                    {
                        "title": "Produtos da Livraria",
                        "icon": "menu_book",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_produtocomercial_changelist')}?modulo__exact=livraria",
                    },
                    {
                        "title": "Vendas Realizadas",
                        "icon": "sell",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_vendacomercial_changelist')}?modulo__exact=livraria",
                    },
                    {
                        "title": "Contas Pendentes (Fiados)",
                        "icon": "request_quote",
                        "link": lambda r: f"{reverse_lazy('admin:usuarios_pendenciacomercial_changelist')}?modulo__exact=livraria",
                    },
                ],
            },
            {
                "title": "Aplicativo Móvel & Controle",
                "separator": True,
                "items": [
                    {
                        "title": "Visibilidade & Exibição no App",
                        "icon": "app_settings_alt",
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