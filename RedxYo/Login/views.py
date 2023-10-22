from django.shortcuts import render,redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
#首頁
#def index(request):
#    return render(request, 'Logins/index.html')





#def sign_in(request):
#    form = LoginForm()
#    if request.method == "POST":
#        username = request.POST.get("username")
#        password = request.POST.get("password")
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return redirect('/')  #重新導向到首頁
#    context = {
#        'form': form
#    }
#    return render(request, 'accounts/login.html', context)

#def sign_in(request):
#    form = LoginForm()
#    context = {
#        'form': form
#    }
#    return render(request, 'Logins/index.html', context)


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 提取用户名和密码
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # 使用authenticate来验证用户
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # 登录用户
                login(request, user)
                # 处理登录成功后的逻辑，例如重定向到其他页面
                return redirect('home')
            else:
                # 处理登录失败的逻辑，例如显示错误消息
                return render(request, 'login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form = AuthenticationForm(request)
    return render(request, 'Logins/index.html', {'form': form})