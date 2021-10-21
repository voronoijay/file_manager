from django.contrib import admin
from .models import StringData

class StringDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(StringData, StringDataAdmin)