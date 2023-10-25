from django.contrib import admin
from .models import Profile
from .models import GeeksModel

admin.site.register(Profile)
class GeeksModelAdmin(admin.ModelAdmin):
    readonly_fields = ['date']  # 将'date'字段添加到readonly_fields中
admin.site.register(GeeksModel, GeeksModelAdmin)