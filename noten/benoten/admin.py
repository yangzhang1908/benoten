from django.contrib import admin

from .models import Question,Choice

# Register my models here.

admin.site.register(Question)
admin.site.register(Choice)
