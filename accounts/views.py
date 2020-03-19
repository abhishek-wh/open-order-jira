from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponse
from pages.models import models
from pages.models import(blocked_user,settings)
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import logout

block_msg=""
def login(request):
    email = ""
    username = ""
    password = ""
    if request.method == 'POST':
        email = request.POST['email_id']
        password = request.POST['password']
        if(email == ""):
            return render(request, 'accounts/login.html', {"msg": "Veuillez saisir votre email"})
        elif(password == ""):
            return render(request, 'accounts/login.html', {"msg": "Veuillez entrer le mot de passe"})
        else:
            try:
                username = User.objects.get(email=email.lower()).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'accounts/login.html',{"msg":"E-mail ou mot de passe incorrect"})
            except:
                return render(request, 'accounts/login.html', {"msg": "E-mail ou mot de passe incorrect"})
    else:
        return render(request, 'accounts/login.html', {"msg": ""})


def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    # return redirect('index')
    return render(request, 'index',)


toggle=False
wctext=""
pid=""
def dashboard(request):
    if request.user.is_authenticated == True:
        blocked_user_record=blocked_user.objects.all()
        for i in range(len(blocked_user_record)):
            print("blocked_user_email",blocked_user_record[i].user_email)

        data=settings.objects.all()
        global toggle
        toggle=data[0].is_jira_app_connected
        global wctext
        wctext=data[0].welcome_text
        global pid
        pid=data[0].jira_project_id

        context = {'toggle': toggle, 'wctext':wctext, 'pid':pid,'blocked_user_record':blocked_user_record,'block_msg':block_msg}

        return render(request, 'accounts/dashboard.html',context)
    else:
        return redirect('login')

    # {% if user.is_authenticatd %}

def dash(request,value):
    data=settings.objects.get(id=1)
    data.is_jira_app_connected=value
    data.save()
    return render(request, 'accounts/dashboard.html')

def settingform(request):
    # if request.method == 'POST':
    welcometext = request.POST['welcometext']
    projectid=request.POST['projectid']
    data = settings.objects.get(id=1)
    data.jira_project_id = projectid
    data.welcome_text = welcometext
    data.save()
    # return render(request, 'accounts/dashboard.html')
    return redirect('dashboard')

def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_pwd']
        if(new_password==confirm_password):
            user = auth.authenticate(username=request.user,password=old_password)
            if user is not None:
                usr = User.objects.get(username=request.user)
                usr.set_password(new_password)
                usr.save()
                return redirect('dashboard')
            else:
                blocked_user_record = blocked_user.objects.all()
                context = {'err_msg': 'Ce mot de passe est incorrect','blocked_user_record':blocked_user_record}
                return render(request, 'accounts/dashboard.html', context)
        else:
            blocked_user_record = blocked_user.objects.all()
            context = {'err_msg': 'Le nouveau mot de passe et la confirmation du mot de passe ne correspondent pas','blocked_user_record':blocked_user_record}
            return render(request, 'accounts/dashboard.html',context)



def block_user(request,value):
    record = blocked_user.objects.filter(user_email=value).exists()
    if(record==True):
        global block_msg
        block_msg="Ya bloqueado"
        return render(request, 'accounts/dashboard.html')
    else:
        data=blocked_user(user_email=value)
        data.save()
        return render(request, 'accounts/dashboard.html')


def unblock_user(request,value):
    data = blocked_user(id=value)
    data.delete()
    return render(request, 'accounts/dashboard.html')







