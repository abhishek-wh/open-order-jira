from django.db import models


class settings(models.Model):
    is_jira_app_connected = models.BooleanField()
    jira_project_id=models.TextField(max_length=200)
    welcome_text=models.TextField(max_length=200,default="WELCOME")
    added_timestamp = models.DateTimeField(auto_now_add=True)


class blocked_user(models.Model):
    user_email = models.EmailField()
    blocked_on=models.DateTimeField(auto_now_add=True)

class logged_in_user(models.Model):
    user_email = models.EmailField()
    logged_on=models.DateTimeField(auto_now_add=True)

class ticket_list(models.Model):
    issue_id=models.TextField(max_length=200,null=True)
    key=models.TextField(max_length=200,null=True)
    issue_type=models.TextField(max_length=200,null=True)
    project=models.TextField(max_length=200,null=True)
    priority=models.TextField(max_length=200,null=True)
    summary=models.TextField(max_length=200,null=True)
    description=models.TextField(max_length=200,null=True)
    assignee=models.TextField(max_length=200,null=True)
    status=models.TextField(max_length=200,null=True)
