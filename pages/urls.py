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
    path('pages/detail/<value>', views.getTicketBykey,name='getTicketBykey'),
    path('pages/detail/add_comment/<value>', views.add_comment,name='getTicketBykey'),
    path('pages/add_attachments', views.add_attachments , name="add_attachments"),
    path('pages/editticket',views.edit_ticket,name='edit_ticket'),
    path('pages/detail/cancelissue/<value>', views.cancelissue,name='cancelissue'),
    path('pages/editticket2',views.edit_ticket2,name='edit_ticket2'),
    path('pages/DownloadZip', views.DownloadZip , name="DownloadZip")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)