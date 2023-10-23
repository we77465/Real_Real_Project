#from django.shortcuts import render
##首頁
#def index(request):
#    return render(request, '1023index.html')




from django.shortcuts import render,redirect,reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#首頁
def index(request):
    return render(request, '1023index.html')
#註冊
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('Test1023/login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, '1023register.html', context)


def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/Test1023/')  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, '1023login.html', context)


def log_out(request):
    logout(request)
    return redirect('/Test1023/login') #重新導向到登入畫面

@login_required(login_url="Login")
def index(request):
    return render(request, '1023index.html')