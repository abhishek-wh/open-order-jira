from django.contrib import admin
from pages.models import (blocked_user,settings,logged_in_user)
admin.site.register(blocked_user)
admin.site.register(settings)
admin.site.register(logged_in_user)

# Register your models here.
