from django.urls import path

from wenba_back import views

app_name = 'wenba_back'

urlpatterns = [
    path('data/detail/', views.detail, name="detail"),
    path('data/index/', views.index, name='index'),
    path('api/addbrowsenum/', views.addbrowsenum, name='addbrowsenum'),
    path('api/addapprovenum/', views.addapprovenum, name='addapprovenum'),
    path('api/addfav/', views.addfav, name='increasefavnum'),
    path('api/reducefav/', views.reducefav, name='decreasefavnum'),
    path('api/register/', views.register, name="register"),
    path('api/login/', views.login, name="login"),
    path('api/changeavatar/', views.changeavatar, name="changeavatar"),
    path('api/search/', views.search, name="search"),
    path('api/getfavs/', views.getfavs, name="getfavs"),
    path('api/judgeisfav/', views.judgeisfav, name="judgeisfav"),
    path('api/addcomment/', views.addcomment, name="addcomment"),
    path('api/getcomments/', views.getcomments, name="getcomments"),
    path('api/approvecomment/', views.approvecomment, name='approvecomment'),
    path('api/cancelapprovecomment/', views.cancelapprovecomment, name="cancelapprovecomment"),
    path('api/addreply/', views.addreply, name="addreply"),
    path('api/comsearch/', views.comsearch, name='comsearch'),
    path('api/getmycomments/', views.getmycomments, name='getmycomments'),
]
