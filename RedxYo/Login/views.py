from django.shortcuts import render
#首頁
def index(request):
    return render(request, 'Logins/index.html')