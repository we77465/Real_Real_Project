from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadeModel
from .forms import UploadeForm

def home(request):
    if request.method == 'POST':
        form = UploadeForm(request.POST, request.FILES)
        if form.is_valid():
            descript = form.cleaned_data['descript']
            password = form.cleaned_data['password']
            original_img = form.cleaned_data['original_img']
            geeks_object = UploadeModel(descript=descript,password = password,
                                         original_img=original_img,user_id = request.user)
            geeks_object.save()  # date字段将自动设置为当前时间
        else:
            form = UploadeForm()
    Uploade_used = UploadeModel.objects.all()
    context = {
        'Uploade_used': Uploade_used,
        'form': UploadeForm(),
    }
    
    return render(request, 'users/home.html', context)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})






from django.http import HttpResponse
from django.conf import settings
from blind_watermark import WaterMark
from io import BytesIO
import os

def download_image(request, image_id): #one_of_Uploade_used.original_img.url
    try:
        image_obj = UploadeModel.objects.get(id=image_id)  # 替换 YourModel 和 id 根据你的模型和数据来定
    except UploadeModel.DoesNotExist:
        return HttpResponse("Image not found", status=404)

    image_path = os.path.join(settings.MEDIA_ROOT, image_obj.original_img.name)
    image_output = os.path.join(settings.MEDIA_ROOT,'images', 'watermarked', image_obj.original_img.name)
    print(image_output)
    # 添加水印

    wm = str(image_obj.user_id)  # 将用户ID转换为整数
    password_wm = 123  # 水印密码
    bwm = WaterMark(password_img=1, password_wm=password_wm)
    bwm.read_img(image_path)
    bwm.read_wm(wm, mode='str')
    
    

    # 添加水印到图像
    bwm.embed(image_path)
    len_wm = len(bwm.wm_bit)
    print(len_wm)

    print("done")

    # 读取带水印的图像
    with open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type="image/jpeg")
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(image_path)}'
        return response

#from django.conf import settings
#import os
# def download_image(request):
#     image_url = request.GET.get('image_url')
#     image_path = os.path.join(settings.MEDIA_ROOT, image_url)
    
#     with open(image_path, 'rb') as image_file:
#         response = HttpResponse(image_file.read(), content_type="image/jpeg")
#         response['Content-Disposition'] = f'attachment; filename={os.path.basename(image_path)}'
#         return response

# from django.http import HttpResponse 這邊為chat GPT生成(未確定可行)的連到DB尋找對應的圖片
# from django.conf import settings
# from yourapp.models import YourModel  # 导入包含图像的模型

# def download_image(request, image_id):
#     try:
#         image_obj = YourModel.objects.get(id=image_id)  # 替换 YourModel 和 id 根据你的模型和数据来定
#     except YourModel.DoesNotExist:
#         return HttpResponse("Image not found", status=404)

#     image_content = image_obj.image_field.read()  # 从数据库中读取图像数据

#     response = HttpResponse(image_content, content_type="image/jpeg")
#     response['Content-Disposition'] = f'attachment; filename={image_obj.image_field.name}'
#     return response