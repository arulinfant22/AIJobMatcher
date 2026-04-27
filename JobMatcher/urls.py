from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('register',views.register,name='sign'),
    path('loginaction',views.loginaction,name='loginaction'),
    path('resume',views.resume,name='resume'),
    path('resumemaker',views.resumemaker,name='resumemaker'),
    path('cover',views.cover,name='cover'),
    path('coverletter', views.coverletter_form, name='coverletter'),
    path('dash',views.dashboard,name='dash'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('dashlogin',views.dashlogin,name='dashlogin'),
    path('resume_upload', views.resume_upload, name='resume_upload'),
    path('logout',views.logout,name='logout')
]