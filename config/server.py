from .settings import *


DEBUG = False

ALLOWED_HOSTS = []

SECRET_KEY = 'nn&5!(a6+cl76#smtmu3n27s-7!rgg3=h&6y0hhxg5zl&o17as'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}