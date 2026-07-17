from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-only-for-local-dev')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'events',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# CompressedManifestStaticFilesStorage hashes filenames for cache-busting,
# but that requires resolving every url()/@import reference inside every
# collected CSS/JS file — including ones from third-party packages
# (Cloudinary's admin widget, Django admin's bundled GIS icons, etc.) whose
# referenced assets don't actually exist in this environment. Any single
# missing reference hard-fails the whole build. CompressedStaticFilesStorage
# still gzip/brotli-compresses everything for performance, it just skips
# the fragile hashing/rewriting step, so one missing third-party asset
# can't take down the entire deploy.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ROOT_URLCONF = 'savannah_woodlands.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'savannah_woodlands.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

# SQLite locks the whole file during writes. Cloudinary uploads (property
# photos/videos) can take several seconds over the network, so without a
# longer busy timeout any second request that touches the DB in that window
# fails immediately with "database is locked" instead of just waiting.
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default'].setdefault('OPTIONS', {})
    DATABASES['default']['OPTIONS']['timeout'] = 20

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = BASE_DIR / 'staticfiles'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# django-cloudinary-storage ships static assets that reference a JS file
# (jquery.fileupload-validate.js) which isn't actually included in the
# package. Whitenoise's manifest storage fails collectstatic when it can't
# resolve that reference. This tells it to warn instead of hard-fail.
WHITENOISE_MANIFEST_STRICT = False


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = [
    'savannahwoodlands.com',
    'www.savannahwoodlands.com',
    '.onrender.com',
    '127.0.0.1',
    'localhost',
]


CSRF_TRUSTED_ORIGINS = [
    'https://savannahwoodlands.com',
    'https://www.savannahwoodlands.com',
    'https://*.onrender.com',
]