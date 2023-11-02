from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from blind_watermark import WaterMark
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, UploadeForm
from .models import UploadeModel,Profile
import os
import re


def home(request):
    if request.method == 'POST':
        form = UploadeForm(request.POST, request.FILES)
        if form.is_valid():
            descript = form.cleaned_data['descript']
            password = form.cleaned_data['password']
            original_img = form.cleaned_data['original_img']
            geeks_object = UploadeModel(descript=descript,password = password,
                                         original_img=original_img,user_id = request.user)
            geeks_object.save() 
        else:
            form = UploadeForm()
    Uploade_used = UploadeModel.objects.all()
    #把Upload_used的資料傳給前端 如果要用就拿Uploade_used
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




from datetime import datetime,timezone,timedelta
def download_image(request, image_id):
    try:
        Profile_all = Profile.objects.all()
        image_obj = UploadeModel.objects.get(id=image_id)
    except UploadeModel.DoesNotExist:
        return HttpResponse("Image not found", status=404)

    image_path = os.path.join(settings.MEDIA_ROOT, image_obj.original_img.name)

    fixed_path = re.sub(r'/', r'\\', image_path)
    print(fixed_path)

    image_output_path = os.path.join(settings.MEDIA_ROOT,'After_mark_images')
    target_path = os.path.join(image_output_path, os.path.basename(image_path))
    print(target_path)

    
    print("start")

    # 添加水印
    wm =("User_ID: ")
    current_user = request.user
    wm += str(current_user.username)
    wm += str("\n download_time : ")
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區
    wm += str(dt2)
    
    password_wm = int(image_obj.password)
    bwm = WaterMark(password_img=1, password_wm=password_wm)
    bwm.read_img(fixed_path)
    bwm.read_wm(wm, mode='str')
    bwm.embed(target_path)  # 在原始图像上添加水印
    len_wm = len(bwm.wm_bit) #要丟到DB裡面



    print("lennn : ",len_wm)
    print("done")
    with open(target_path, 'rb') as image_file:
        image_data = image_file.read()

    # 返回
    response = HttpResponse(image_data, content_type="image/jpeg")
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(image_path)}'
    return response



def delete_image(request, image_id):
    try:
        instance = UploadeModel.objects.get(id=image_id)
        instance.delete()
    except UploadeModel.DoesNotExist:
        pass

    Uploade_used = UploadeModel.objects.all()
    context = {
        'Uploade_used': Uploade_used,
        'form': UploadeForm(),
    }


    return render(request, 'users/home.html', context)

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

