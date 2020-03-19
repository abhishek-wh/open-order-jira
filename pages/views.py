from django.shortcuts import render, redirect, HttpResponse
from .models import (blocked_user, settings, logged_in_user, ticket_list)
import requests
from requests.auth import HTTPBasicAuth
import json
from django.core.paginator import Paginator
import jira
from jira.client import JIRA
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings as setting
from django.http import HttpResponse

url = "https://nrc.atlassian.net/rest/api/2/"
auth = HTTPBasicAuth("contact@wowdesigns.fr", "guPJmBOx3nVhEWMFogxRAB84")

# url = "https://dishanshujagtap.atlassian.net/rest/api/2/"
# auth = HTTPBasicAuth("dishanshu.jagtap@webhungers.com", "edItHS8Dbnh0XkkTWQjoFE45")

def index(request):
    data = settings.objects.all()
    welcome_text = data[0].welcome_text
    msg = ""
    if request.method == 'POST':
        username = request.POST['em']
        is_user = blocked_user.objects.filter(user_email=username).exists()
        if (is_user == False):
            is_jira_connect = settings.objects.filter(is_jira_app_connected=False).exists()
            if (is_jira_connect):
                request.session['username'] = username
                return redirect('pages/dashboard')
                # jira_api = getUser(username)      
                # if (jira_api['status_code'] == 200):
                #     record1 = logged_in_user.objects.all()
                #     record = logged_in_user.objects.all().exists()
                #     if (record == True):
                #         request.session['username'] = username
                #     else:
                #         logged_in_user(user_email=username).save()
                #     return redirect('pages/dashboard')
                # else:
                #     msg = "Cet utilisateur n'est pas en jira"
            else:
                msg = "Pas connecté"
        else:
            msg = "Utilisateur bloqué"

    context = {'var': msg, 'welcome_text': 'welcome_text'}

    return render(request, 'pages/index.html', context)


def getUser(user_id):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request(
        "get",
        url + "user?username=" + user_id,
        headers=headers,
        auth=auth
    )


    return vars(response)


def dashboard(request):
    if request.session.has_key('username'):
        username = request.session['username']
        issues = getTicketByUsername(username)
        ticket_list.objects.all().delete()
        for issue in issues:
            desc = ""
            assi = ""
            try:
                desc = issue.raw['fields']['description']
            except:
                desc = ""
            try:
                assi = issue.raw['fields']['assignee']['displayName']
            except:
                assi = ""

            ticket_list.objects.create(issue_id=str(issue.raw['id']),
                                       key=issue.raw['key'],
                                       issue_type=issue.raw['fields']['issuetype']['name'],
                                       project=issue.raw['fields']['project']['name'],
                                       priority=issue.raw['fields']['priority']['name'],
                                       summary=issue.raw['fields']['summary'],
                                       description=desc,
                                       assignee=assi,
                                       status=issue.raw['fields']['status']['statusCategory']['name']).save()
        t_list = ticket_list.objects.all()

        try:
            flag = True
        except:
            flag = False
        paginator = Paginator(t_list, 5)  # Show 5 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'user_email': username, 'flag': flag}
        return render(request, 'pages/dashboard.html', context)
        # return render(request, 'pages/index.html')
    else:
        return render(request, 'pages/index.html')



def getTicketByUsername(email_id):
    jira_options={'server': 'https://nrc.atlassian.net/'}
    jira=JIRA(options=jira_options,basic_auth=('contact@wowdesigns.fr','guPJmBOx3nVhEWMFogxRAB84'))  
    # issues=jira.search_issues("project='ORDER' and reporter='"+user_id+"'")
    issues = jira.search_issues(" cf[10039]= '"+email_id+"' ")
    return issues
a=""
def getTicketBykey(request,value):
    global a
    a=value
    comments=add_comment("","")
    jira_options={'server': 'https://nrc.atlassian.net/'}
    jira=JIRA(options=jira_options,basic_auth=('contact@wowdesigns.fr','guPJmBOx3nVhEWMFogxRAB84'))
    issues=jira.search_issues("issue="+value)
    issues_detail=""
    for i in issues:
        issues_detail=i.raw['fields']['status']['statusCategory']['name']
    context = {'issues_detail': issues_detail,'order_number':value,'details':i.raw,'comments':comments}
    return render(request, 'pages/detail.html',context)




def add_comment(request,value):
    global a

    if len(value)!=0:
        jira_options = {'server': 'https://nrc.atlassian.net/'}
        jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84'))
        comments = jira.comments(a)
        for comment in comments:
            comment = jira.add_comment(a, value)
        # jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84'))
        # comment = jira.add_comment("ORDER-129", value)

        comments = jira.comments(a)
    else:
        jira_options = {'server': 'https://nrc.atlassian.net/'}
        jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84'))

        comments = jira.comments(a)
        recent_comment=[]
        for comment in comments:
            recent_comment.append(comment)
    # return render(request, 'pages/detail.html',{})
    return comments


# def createTicketByUsername(request,ticket_title,issue_description):
#     user_id = request.session['username']
#     jira_options={'server': 'https://nrc.atlassian.net/'}
#     jira=JIRA(options=jira_options,basic_auth=('contact@wowdesigns.fr','guPJmBOx3nVhEWMFogxRAB84'))  
#     new_issue = jira.create_issue(project='ORDER', summary=ticket_title, description=issue_description, issuetype={"name": "Commande"})
#     return render(request, 'accounts/dashboard.html')    


def search(request,value):
    flag=False
    if(value=='All'):
        if request.session.has_key('username'):
            username = request.session['username']
            issues = getTicketByUsername(username)
            ticket_list.objects.all().delete()
            for issue in issues:
                desc = ""
                assi = ""
                try:
                    desc = issue.raw['fields']['description']
                except:
                    desc = ""
                try:
                    assi = issue.raw['fields']['assignee']['displayName']
                except:
                    assi = ""

                ticket_list.objects.create(issue_id=str(issue.raw['id']),
                                        key=issue.raw['key'],
                                        issue_type=issue.raw['fields']['issuetype']['name'],
                                        project=issue.raw['fields']['project']['name'],
                                        priority=issue.raw['fields']['priority']['name'],
                                        summary=issue.raw['fields']['summary'],
                                        description=desc,
                                        assignee=assi,
                                        status=issue.raw['fields']['status']['statusCategory']['name']).save()
            t_list = ticket_list.objects.all()

            try:
                flag = True
            except:
                flag = False
            paginator = Paginator(t_list, 5)  # Show 5 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'page_obj': page_obj,'user_email':username,'flag':flag}
            return render(request, 'pages/dashboard.html', context)
        else:
            return render(request, 'pages/index.html')
    else:
        if request.session.has_key('username'):
            username = request.session['username']
            t_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list where issue_id like '%"+value+"%' or key LIKE '%"+value+"%' OR issue_type LIKE '%"+value+"%' OR project LIKE '%"+value+"%' OR priority LIKE '%"+value+"%' OR description LIKE '%"+value+"%' OR assignee LIKE '%"+value+"%' OR status LIKE '%"+value+"%' or summary LIKE '%"+value+"%'")
            try:
                flag=True
            except:
                flag=False
            paginator = Paginator(t_list, 10) # Show 10 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'page_obj': page_obj,'user_email':username,'flag':flag}
            return render(request, 'pages/dashboard.html', context)
        else:
            return render(request, 'pages/index.html')


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    data = settings.objects.all()
    welcome_text = data[0].welcome_text
    context = {'welcome_text': welcome_text}

    return render(request, 'pages/index.html', context)


def create_ticket(request):      
    if request.method == 'POST':
        username = request.session['username']
        sdata = settings.objects.all()
        project_id=sdata[0].jira_project_id
        jira_options = {'server': 'https://nrc.atlassian.net/'}
        jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84'))
        
        # myfile1 = request.FILES['attachment']
        # fs = FileSystemStorage(location=setting.MEDIA_ROOT) #defaults to MEDIA_ROOT  
        # filename = fs.save(myfile1.name, myfile1)
        # file_url = fs.url(filename)

        new_issue = jira.create_issue(project=project_id,
        summary=request.POST.get('ticket_title',""),
        description=request.POST.get('description',""),
        issuetype={"name": "Commande"},
        customfield_10039=[username],
        customfield_10077=request.POST.get('enterprise',""),
        customfield_10032=request.POST.get('firstname',""),
        customfield_10033=request.POST.get('lastname',""),
        customfield_10037=request.POST.get('phone',""),
        customfield_10040=[request.POST.get('mailcopy',"")],
        customfield_10041=request.POST.get('provider',""),
        customfield_10042=request.POST.get('provider_web_link',""),
        customfield_10078=request.POST.get('place',""),
        customfield_10050=request.POST.get('deliver_address',""),
        customfield_10058=request.POST.get('postal_code',""),
        customfield_10052=request.POST.get('city',""),
        customfield_10053=request.POST.get('deliver_name',""),
        customfield_10054=request.POST.get('phone_delivery',""),
        customfield_10076=request.POST.get('instruction',""))

        
        
        # res=add_attachments(str(new_issue),file_url)
        
        res=str(new_issue)
        return HttpResponse(res)
    else:
        username = request.session['username']
        context = {'user_email': username}
        return render(request,'pages/createticket.html',context)

def add_attachments(issue_key, doc_file):
    jira_options={'server': 'https://nrc.atlassian.net/'}
    jira=JIRA(options=jira_options,basic_auth=('contact@wowdesigns.fr','guPJmBOx3nVhEWMFogxRAB84'))
    result=""
    with open('/home/user/Desktop/abhishek joshi/projects/open system/OpenSys/OpenSys/'+doc_file, 'rb') as f:
        result=jira.add_attachment(issue=issue_key, attachment=f)
    return result

def create(request):    
    
    return render(request,'pages/createticket.html')
