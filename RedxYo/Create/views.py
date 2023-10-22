from django.shortcuts import render,redirect

# Create your views here.
#def showtemplate(request):
#    # 今天先不探討什麼是 render，先記得它會去撈 test.html
#    return render(request, 'test.html')



from .models import Account
# # Create your views here.
# def showtemplate(request):
#     Account_list = Account.objects.all() # 把所有 Vendor 的資料取出來
#     context = {'Account_list': Account_list} # 建立 Dict對應到Vendor的資料，
#     return render(request, 'Creates/create_tetail.html', context)

from .forms import AccountForm
def showtemplate(request):
    form = AccountForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login')

    context = {
        'form' : form
    } # 建立 Dict對應到Vendor的資料，
    return render(request, 'Creates/1022_test.html', context)
    