from functools import wraps
from django.core.exceptions import PermissionDenied
from .models import GeneratedToken


def check_token(view_func):
    @wraps(view_func)
    def new_view_func(request,*args, **kwargs):
        tokens = GeneratedToken.objects.all().filter(token=kwargs['token'])
        if tokens.exists():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return new_view_func
