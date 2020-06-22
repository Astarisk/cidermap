from django.contrib import admin
from .models import Grid, MarkerData, LostMarkerData, CharacterLocation, GeneratedToken


# Register your models here.
admin.site.register(Grid)
admin.site.register(MarkerData)
admin.site.register(LostMarkerData)
admin.site.register(CharacterLocation)
admin.site.register(GeneratedToken)

