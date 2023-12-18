from django.contrib import admin

# Register your models here.

from .models import Participant, DrawNames, DrawName

admin.site.register(Participant)
admin.site.register(DrawNames)
admin.site.register(DrawName)