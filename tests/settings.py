INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'django_keyerror',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_keyerror.middleware.KeyErrorMiddleware',
)

SECRET_KEY = 'test'
ROOT_URLCONF = 'tests.urls'

LOGGING = {
    'version': 1,
    'loggers': {'': {'level': 'CRITICAL'}},
}

KEYERROR_ENABLED = True
KEYERROR_SECRET_KEY = 'd4bacc4efc5a6c0ac389cca5574ea7ec7e8418dc'
