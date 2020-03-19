from django.urls import path
from .import views


urlpatterns = [
    path('login',views.login, name='login'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('dash/<value>', views.dash,name='dash'),
    path('block_user/<value>', views.block_user,name='block_user'),
    path('unblock_user/<value>', views.unblock_user,name='unblock_user'),
    path('settingform', views.settingform,name='settingform'),
    path('changepassword', views.changepassword,name='changepassword'),

]