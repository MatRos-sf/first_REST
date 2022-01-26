from django.contrib import admin
from .models import Film, ExtraInfo, Recenzja, Aktor
# Register your models here.

admin.site.register(Film)
admin.site.register(ExtraInfo)
admin.site.register(Recenzja)
admin.site.register(Aktor)