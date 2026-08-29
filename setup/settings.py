import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

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
    "SITE_HEADER": "CDM Gestão Ministerial",
    "SITE_URL": "/",
    "SITE_SYMBOL": "church",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "STYLES": [
        lambda request: "css/custom_cdm.css?v=4", 
    ],
    "COLORS": {
        "primary": {
            "50": "235 248 255",
            "100": "206 240 253",
            "200": "157 226 252",
            "300": "0 163 224",    # Ciano CDM (#00A3E0)
            "400": "0 130 200",
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
                        "icon": "people",
                        "link": lambda request: "/admin/usuarios/cadastrogeral/",
                    },
                    {
                        "title": "Usuários do Sistema",
                        "icon": "badge",
                        "link": lambda request: "/admin/usuarios/usuario/",
                    },
                    {
                        "title": "Jornada do Membro",
                        "icon": "timeline",
                        "link": lambda request: "/admin/usuarios/jornadacadastro/",
                    },
                    {
                        "title": "Landing Pages Avulsas",
                        "icon": "web",
                        "link": lambda request: "/admin/usuarios/formularioavulso/",
                    },
                ],
            },
            {
                "title": "Células / Grupos de Conexão",
                "separator": True,
                "items": [
                    {
                        "title": "Grupos de Conexão (GCs)",
                        "icon": "diversity_3",
                        "link": lambda request: "/admin/usuarios/grupoconexao/",
                    },
                    {
                        "title": "Lançamentos Semanais",
                        "icon": "event_available",
                        "link": lambda request: "/admin/usuarios/gclancamentosemanal/",
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
                        "link": lambda request: "/admin/usuarios/idemodulo/",
                    },
                    {
                        "title": "Turmas Ativas",
                        "icon": "groups",
                        "link": lambda request: "/admin/usuarios/ideturma/",
                    },
                    {
                        "title": "Inscrições nos Cursos",
                        "icon": "how_to_reg",
                        "link": lambda request: "/admin/usuarios/ideinscricao/",
                    },
                    {
                        "title": "Diário de Aulas / Presenças",
                        "icon": "assignment",
                        "link": lambda request: "/admin/usuarios/idesala/",
                    },
                    {
                        "title": "Formulários de Matrícula",
                        "icon": "feed",
                        "link": lambda request: "/admin/usuarios/ideformulario/",
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
                        "link": lambda request: "/admin/usuarios/ministerio/",
                    },
                    {
                        "title": "Voluntários Registrados",
                        "icon": "assignment_ind",
                        "link": lambda request: "/admin/usuarios/voluntario/",
                    },
                    {
                        "title": "Escalas & Eventos",
                        "icon": "event_note",
                        "link": lambda request: "/admin/usuarios/escalaministerio/",
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
                        "link": lambda request: "/admin/usuarios/produtocomercial/",
                    },
                    {
                        "title": "Vendas Concluídas",
                        "icon": "point_of_sale",
                        "link": lambda request: "/admin/usuarios/vendacomercial/",
                    },
                    {
                        "title": "Contas Pendentes (Fiados)",
                        "icon": "pending_actions",
                        "link": lambda request: "/admin/usuarios/pendenciacomercial/",
                    },
                    {
                        "title": "Contas a Pagar",
                        "icon": "request_quote",
                        "link": lambda request: "/admin/usuarios/contapagarcomercial/",
                    },
                    {
                        "title": "Entradas de Estoque",
                        "icon": "move_to_inbox",
                        "link": lambda request: "/admin/usuarios/entradaestoquecomercial/",
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
                        "link": lambda request: "/admin/usuarios/filanotificacaopush/",
                    },
                    {
                        "title": "Configurações Globais",
                        "icon": "settings",
                        "link": lambda request: "/admin/usuarios/configuracaosistema/",
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
    'whitenoise.middleware.WhiteNoiseMiddleware', 
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

STATIC_URL = 'static/'
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