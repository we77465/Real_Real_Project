from django.contrib import admin
from .models import Profile
from .models import UploadeModel

admin.site.register(Profile)
class UploadeModelAdmin(admin.ModelAdmin):
    readonly_fields = ['date']  # 将'date'字段添加到readonly_fields中
admin.site.register(UploadeModel, UploadeModelAdmin)