from django.contrib import messages
from django.contrib.auth import login

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import RegisterForm
from users.models import User


def register(request):
    #获取跳转地址
    redirect_to = request.POST.get('next',request.GET.get('next',''))
    form = RegisterForm()
    if request.method == 'POST':
        #首先使用提交的数据生成form
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            #返回登入，并提示注册成功，
            messages.success(request,'注册成功，欢迎来到登入界面')
            if redirect_to:
                login(request,user)
                return redirect(redirect_to)
            else:
                #重定向到login
                return redirect(reverse('login'))
    else:
        return render(request,'users/register.html',{'form':form,'next':redirect_to})
    pass
def detail(request):
    user = request.user
    pass

class EditUserView(UpdateView):
    model = User
    # template_name = ''
    fields = ['nickname', 'email', 'headshot', 'signature']
    # form_class = RegisterForm
    success_url = reverse_lazy('blog:index')
    pass