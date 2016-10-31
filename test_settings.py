INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',

    'django_keyerror',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SECRET_KEY = 'test'
ROOT_URLCONF = 'test_urls'

LOGGING = {
    'version': 1,
    'loggers': {'': {'level': 'CRITICAL'}},
}

KEYERROR_SECRET_KEY = 'test'