"""web1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.global_settings import STATIC_ROOT
from django.contrib import admin
from django.urls import path
from django.urls import  re_path
from django.conf import settings
from django.conf.urls.static import static
from web1.settings import STATIC_URL
from myblog import views
from myblog import api

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/login',api.LoginView.as_view()),
    re_path('api/profile',api.ProfileView.as_view()),
    re_path('api/ini',api.IniView.as_view()),
    re_path('api/upload',api.UploadView.as_view()),
    re_path('api/list',api.ListView.as_view()),
    re_path('api/re_detail',api.DetailView.as_view()),
    re_path('api/comment',api.CommentView.as_view()),
    re_path('api/collect',api.CollectView.as_view())
    #index函数不加括号

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#static使访问时可以路由到对应文件夹
