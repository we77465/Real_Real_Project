from django.db import models
from django.contrib import admin

# Create your models here.
class Account(models.Model):
	Username = models.CharField(max_length = 20) # 攤販的名稱
	Password = models.CharField(max_length = 10) # 攤販店家的名稱
	EmailAddress = models.CharField(max_length = 100) # 攤販的地址
	
	def __str__(self):
		return self.Username

class AccountAdmin(admin.ModelAdmin):
	list_display = ('id', 'Username') 