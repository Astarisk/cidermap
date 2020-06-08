from django.contrib import admin
from .models import GridData, MarkerData, LostMarkerData, CharacterLocation, GeneratedToken


# Register your models here.
admin.site.register(GridData)
admin.site.register(MarkerData)
admin.site.register(LostMarkerData)
admin.site.register(CharacterLocation)
admin.site.register(GeneratedToken)

