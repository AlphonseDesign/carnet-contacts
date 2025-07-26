from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Clé secrète (à définir dans les variables Render)
SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme-in-local-dev')

# ✅ Mode production désactivé par défaut
DEBUG = False

# ✅ Domaine Render autorisé
ALLOWED_HOSTS = ['.onrender.com']

# ✅ Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contacts.apps.ContactsConfig',
]

# ✅ Middleware standard
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ URLs et WSGI
ROOT_URLCONF = 'carnet.urls'
WSGI_APPLICATION = 'carnet.wsgi.application'

# ✅ Templates (avec répertoire personnalisé)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'contacts', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ✅ Base de données SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ Validateurs de mot de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Langue et fuseau
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Fichiers statiques (logo, CSS, JS...)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'contacts', 'static'),  # ➕ TON dossier où est le logo
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ➕ pour Render

# ✅ Médias (si tu ajoutes des fichiers uploadés par l’utilisateur)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ Authentification
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/accueil/'
