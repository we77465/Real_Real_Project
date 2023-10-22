from django.shortcuts import render

# Create your views here.
def showtemplate(request):
    # 今天先不探討什麼是 render，先記得它會去撈 test.html
    return render(request, 'test.html')