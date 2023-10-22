from django.shortcuts import render
from .forms import LoginForm
#首頁
#def index(request):
#    return render(request, 'Logins/index.html')

def sign_in(request):
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'Logins/index.html', context)