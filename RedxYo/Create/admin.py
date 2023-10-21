from django.contrib import admin

# Register your models here.

from .models import Account,AccountAdmin

# Register your models here.
admin.site.register(Account,AccountAdmin)