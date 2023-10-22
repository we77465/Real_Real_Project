from django import forms
from django.db import models
from .models import Account

from django.utils.translation import gettext_lazy as _ # 新增

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        # 新增 labels 對應
        labels = {
            'Username': _('帳號'),
            'Password' : _('密碼'),
            'EmailAddress' : _('電子信箱'),
        }