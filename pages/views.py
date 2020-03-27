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
from bootstrap_daterangepicker import widgets, fields


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

    data = settings.objects.all()
    welcome_text = data[0].welcome_text
    context = {'var': msg,'welcome_text': welcome_text}
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
        block_count=0
        for issue in issues: 
            assi = ""           
            try:
                assi = issue.raw['fields']['assignee']['displayName']
            except:
                assi = ""

            status=""
            if(issue.raw['fields']['status']['statusCategory']['name']=='Terminé'):
                if(issue.raw['fields']['status']['name'] == 'Bloqué'):
                    block_count=block_count+1
                if(issue.raw['fields']['status']['name'] == 'Bloqué' or issue.raw['fields']['status']['name'] == 'Annulé'):
                    status=issue.raw['fields']['status']['name']
                else:
                    status=issue.raw['fields']['status']['statusCategory']['name']
            else:
                status=issue.raw['fields']['status']['statusCategory']['name']
            ticket_list.objects.create(key=issue.raw['key'],                                       
                                       summary=issue.raw['fields']['summary'],
                                       suplier=issue.raw['fields']['customfield_10041'],
                                       status=status,                     
                                       created=str(issue.raw['fields']['created']).split('T')[0],
                                       updated=str(issue.raw['fields']['updated']).split('T')[0],
                                       assignee=assi).save()
        
        t_list = ticket_list.objects.all()
        lt_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list order by created DESC LIMIT 5")
        
        try:
            if(ticket_list.objects.all().exists()):                
                flag = True
            else:
                flag = False
        except:
            flag = False
        paginator = Paginator(t_list, 5)  # Show 5 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'user_email': username, 'flag': flag, 'lt_list':lt_list, 'block_count':block_count}
        return render(request, 'pages/dashboard.html', context)
        # return render(request, 'pages/index.html')
    else:
        return render(request, 'pages/index.html')



def getTicketByUsername(email_id):
    sdata = settings.objects.all()
    project_id=sdata[0].jira_project_id
    jira_options={'server': 'https://nrc.atlassian.net/'}
    jira=JIRA(options=jira_options,basic_auth=('contact@wowdesigns.fr','guPJmBOx3nVhEWMFogxRAB84'))  
    # issues=jira.search_issues("project='ORDER' and reporter='"+user_id+"'")
    issues=''
    try:
        issues = jira.search_issues(" project='"+project_id+"' and cf[10039]= '"+email_id+"' ")
    except:
        issues=''
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
        # issues_detail=i.raw['fields']['status']['statusCategory']['name']
        # issue_status=i.raw['fields']['status']['name']
        if(i.raw['fields']['status']['statusCategory']['name']=='Terminé'):
            issues_detail=i.raw['fields']['status']['statusCategory']['name']
            if(i.raw['fields']['status']['name'] == 'Bloqué' or i.raw['fields']['status']['name'] == 'Annulé'):
                issues_detail=i.raw['fields']['status']['name']
                issue_status=i.raw['fields']['status']['name']
            else:
                issues_detail=i.raw['fields']['status']['statusCategory']['name']
                issue_status=i.raw['fields']['status']['name']
        else:
            issues_detail=i.raw['fields']['status']['statusCategory']['name']
            issue_status=i.raw['fields']['status']['name']

    #attachments
    jira_filename=""
    jira_issue = jira.issue( value, expand = "attachment")
    print("jira_issuess",jira_issue)
    for attachment in jira_issue.fields.attachment:
        image = attachment.get()
        jira_filename = attachment.filename
        print("cesvcsdv", jira_filename)
        with open(jira_filename, 'wb') as f:
            f.write(image)
    flag=False
    print("cesvcsdv", jira_filename)
    if(jira_filename!=""):
        flag=True
    else:
        jira_filename=""

    context = {'issues_detail': issues_detail,'issue_status':issue_status,'order_number':value,'details':i.raw,'comments':comments,"jira_filename":jira_filename,"flag":flag}
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

def cancelissue(request,value):
    jira_options = {'server': 'https://nrc.atlassian.net/'}
    jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84'))
    jira.transition_issue(value, transition='141')
    return render(request,'pages/detail.html')

def search(request,value):
    flag=False
    if(value=='All'):
        block_count=0
        if request.session.has_key('username'):
            username = request.session['username']
            issues = getTicketByUsername(username)
            ticket_list.objects.all().delete()
            for issue in issues:
                assi = ""           
                try:
                    assi = issue.raw['fields']['assignee']['displayName']
                except:
                    assi = ""

                if(issue.raw['fields']['status']['statusCategory']['name']=='Terminé'):
                    if(issue.raw['fields']['status']['name'] == 'Bloqué'):
                        block_count=block_count+1
                    if(issue.raw['fields']['status']['name'] == 'Bloqué' or issue.raw['fields']['status']['name'] == 'Annulé'):
                        status=issue.raw['fields']['status']['name']
                    else:
                        status=issue.raw['fields']['status']['statusCategory']['name']
                else:
                    status=issue.raw['fields']['status']['statusCategory']['name']
                ticket_list.objects.create(key=issue.raw['key'],                                       
                                       summary=issue.raw['fields']['summary'],
                                       suplier=issue.raw['fields']['customfield_10041'],
                                       status=status,                     
                                       created=str(issue.raw['fields']['created']).split('T')[0],
                                       updated=str(issue.raw['fields']['updated']).split('T')[0],
                                       assignee=assi).save()
            t_list = ticket_list.objects.all()
            lt_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list order by created DESC LIMIT 5")
            try:
                flag = True
            except:
                flag = False
            paginator = Paginator(t_list, 5)  # Show 5 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'page_obj': page_obj,'user_email':username,'flag':flag, 'searchkey':'', 'lt_list':lt_list,'block_count':block_count}
            return render(request, 'pages/dashboard.html', context)
        else:
            return render(request, 'pages/index.html')
    else:
        if request.session.has_key('username'):
            block_count=0
            username = request.session['username']
            if(value=='En cours' or value=='Terminé' or value=='Annulé' or value=='bloquée'):                
                lt_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list order by created DESC LIMIT 5")
                t_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list where key like '%"+value+"%' or summary LIKE '%"+value+"%' OR suplier LIKE '%"+value+"%' OR status LIKE '%"+value+"%' OR created LIKE '%"+value+"%' OR updated LIKE '%"+value+"%' OR assignee LIKE '%"+value+"%'")
                try:
                    flag=True
                except:
                    flag=False
                paginator = Paginator(t_list, 10) # Show 10 contacts per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                if(value=='In Progress' or value=='Done' or value=='Cancelled' or value=='Notification' or value=='Creation'):
                    value=""
                for dt in ticket_list.objects.all():
                    if(dt.status == 'Bloqué'):
                        block_count=block_count+1
                context = {'page_obj': page_obj,'user_email':username,'flag':flag, 'searchkey':'', 'lt_list':lt_list,'block_count':block_count}
                return render(request, 'pages/dashboard.html', context)
            else:
                flagg=False
                try:
                    flagg=True
                    from_dt=str(value.split("to")[0])
                    to_dt=str(value.split("to")[1])
                    lt_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list order by created DESC LIMIT 5")
                    t_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list WHERE Created BETWEEN '"+from_dt+"' AND '"+to_dt+"'")
                except:
                    flagg=False
                    lt_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list order by created DESC LIMIT 5")
                    t_list=ticket_list.objects.raw("SELECT * FROM pages_ticket_list where key like '%"+value+"%' or summary LIKE '%"+value+"%' OR suplier LIKE '%"+value+"%' OR status LIKE '%"+value+"%' OR created LIKE '%"+value+"%' OR updated LIKE '%"+value+"%' OR assignee LIKE '%"+value+"%'")
                try:
                    flag=True
                except:
                    flag=False
                paginator = Paginator(t_list, 10) # Show 10 contacts per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                if(value=='In Progress' or value=='Done' or value=='Cancelled' or value=='Notification' or value=='Creation'):
                    value=""
                for dt in ticket_list.objects.all():
                    if(dt.status == 'Bloqué'):
                        block_count=block_count+1
                if(flagg):                                       
                    context = {'page_obj': page_obj,'user_email':username,'flag':flag, 'searchkey':'','searchdate':' ('+value.split("to")[0]+' to '+value.split("to")[1]+')', 'lt_list':lt_list,'block_count':block_count}
                else:
                    context = {'page_obj': page_obj,'user_email':username,'flag':flag, 'searchkey':value, 'lt_list':lt_list,'block_count':block_count}
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
    file_url=""
    if request.method == 'POST':
        username = request.session['username']
        sdata = settings.objects.all()
        project_id=sdata[0].jira_project_id
        jira_options = {'server': 'https://nrc.atlassian.net/'}
        jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84')) 
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
        res=str(new_issue)        
        return HttpResponse(res)
    else:
        username = request.session['username']
        context = {'user_email': username}
        return render(request,'pages/createticket.html',context)

def edit_ticket(request):  
    if request.method == 'POST':
        sdata = settings.objects.all()
        project_id=sdata[0].jira_project_id
        jira_options = {'server': 'https://nrc.atlassian.net/'}
        jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84')) 
        issuekey=request.POST.get('issuekey',"")
        cf33=request.POST.get('lastname',"")
        cf32=request.POST.get('firstname',"")
        cf77=request.POST.get('enterprise',"")
        cf37=request.POST.get('phone',"")
        cf40=request.POST.get('backupmail',"")
        description=request.POST.get('description',"")
        jira.issue(issuekey).update(fields={'customfield_10033': cf33, 'customfield_10032': cf32,'customfield_10077': cf77,'customfield_10037': cf37,'customfield_10040': [cf40],'description':description })
        return render(request,'pages/detail.html')
    else:        
        return render(request,'pages/detail.html')

def edit_ticket2(request):  
    if request.method == 'POST':
        sdata = settings.objects.all()
        project_id=sdata[0].jira_project_id
        jira_options = {'server': 'https://nrc.atlassian.net/'}
        jira = JIRA(options=jira_options, basic_auth=('contact@wowdesigns.fr', 'guPJmBOx3nVhEWMFogxRAB84')) 
        issuekey=request.POST.get('issuekey',"")
        cf53=request.POST.get('cf53',"")
        cf54=request.POST.get('cf54',"")
        cf78=request.POST.get('cf78',"")
        cf50=request.POST.get('cf50',"")
        cf58=request.POST.get('cf58',"")
        cf52=request.POST.get('cf52',"")
        cf76=request.POST.get('cf76',"")
        cf55=request.POST.get('cf55',"")
        jira.issue(issuekey).update(fields={'customfield_10053': cf53, 'customfield_10054': cf54,'customfield_10078': cf78,'customfield_10050': cf50,'customfield_10058': cf58,'customfield_10052':cf52,'customfield_10076':cf76,'customfield_10055':cf55 })
        return render(request,'pages/detail.html')
    else:        
        return render(request,'pages/detail.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def add_attachments(request):
    myfile1 = request.FILES['attachment']
    fs = FileSystemStorage(location=setting.MEDIA_ROOT) #defaults to MEDIA_ROOT  
    filename = fs.save(myfile1.name, myfile1)
    file_url = fs.url(filename)
    jira_options={'server': 'https://nrc.atlassian.net/'}
    jira=JIRA(options=jira_options,basic_auth=('contact@wowdesigns.fr','guPJmBOx3nVhEWMFogxRAB84'))
    result=""
    with open('/home/user/Desktop/abhishek joshi/projects/open system/OpenSys/OpenSys/'+file_url, 'rb') as f:
        result=jira.add_attachment(issue=request.POST.get('ticketkey',""), attachment=f)
    return result

def create(request):        
    return render(request,'pages/createticket.html')
