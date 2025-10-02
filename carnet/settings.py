from pathlib import Path
import os
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SÉCURITÉ ET HOSTING
# Utilise la variable d'environnement pour la clé secrète.
# La valeur par défaut est celle de développement (à ne JAMAIS utiliser en prod).
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-umi10be49hr*wqhvaasn@uu!dgf7+^0y$tr@=hu9iv+0r5am1_')

# Le mode DEBUG est désactivé en production (Render le gérera avec une variable d'environnement).
# On force le mode 'True' uniquement si la variable d'environnement est 'True'.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Si DEBUG est False (en production), on ajoute l'hôte de Render en dur.
if not DEBUG:
    # Assurez-vous que cette URL est EXACTEMENT celle que vous voyez dans l'erreur.
    ALLOWED_HOSTS.append('carnet-contacts.onrender.com')

# Récupérer l'URL de Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    # L'URL de Render sans le sous-domaine
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME.split(':')[0])

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contacts.apps.ContactsConfig',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise doit être placé après SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'carnet.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'contacts' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'contacts.context_processors.entreprise_utilisateur',
            ],
        },
    },
]

WSGI_APPLICATION = 'carnet.wsgi.application'

# BASE DE DONNÉES
# Utilise une connexion Postgresql sur Render, sinon utilise SQLite en local
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# VALIDATEURS DE MOTS DE PASSE
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALISATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# FICHIERS STATIQUES ET MÉDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REDIRECTIONS
LOGIN_REDIRECT_URL = 'accueil'
LOGOUT_REDIRECT_URL = 'login'

# CORRECTION DE LA BDD (si vous n'avez pas de clé pour la bdd dans votre BDD Render)
if os.environ.get('DATABASE_URL') and 'sqlite' not in os.environ.get('DATABASE_URL'):
    del DATABASES['default']['NAME']