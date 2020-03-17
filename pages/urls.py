from django.urls import path
from .import views

#import for Media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[

    path('index',views.index,name='index'),
    path('pages/dashboard',views.dashboard,name='dashboard'),
    path('pages/dashboard/<value>', views.search,name='search'),
    path('pages/logout', views.logout, name = 'logout'),
    path('pages/createticket',views.create_ticket,name='create_ticket'),
    path('pages/create',views.create,name='create'),
    # path('pages/createTicketByUsername/<ticket_title>/<issue_description>', views.createTicketByUsername,name='createTicketByUsername'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)