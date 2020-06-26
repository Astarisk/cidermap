from .settings import *


DEBUG = False

ALLOWED_HOSTS = []

SECRET_KEY = 'nn&5!(a6+cl76#smtmu3n27s-7!rgg3=h&6y0hhxg5zl&o17as'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my-app-db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': 3306,
    }
}
