from django.contrib import admin

from .models import AiLog, AiParsedItem

admin.site.register(AiLog)
admin.site.register(AiParsedItem)
