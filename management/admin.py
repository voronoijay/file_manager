from django.contrib import admin
from .models import StringData

class StringDataAdmin(admin.ModelAdmin):
    show_full_result_count = False

admin.site.register(StringData, StringDataAdmin)