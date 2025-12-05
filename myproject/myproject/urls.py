"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from basic.views import sample
from basic.views import sample1
from basic.views import sampleInfo
from basic.views import dynamicresponse
from basic.views import health
from basic.views import addStudent
from basic.views import addPost,signUp,check,login,hash_all_passwords,getAllusers,homerequest,aboutus,welcome,services,contact,projects


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sample/',sample),
    path('sample1/',sample1),
    path('sampleInfo/',sampleInfo),
    path('dynamicresponse/',dynamicresponse),
    path('health/',health),
    path('student/',addStudent),
    path('addpost/',addPost),
    # path('job1/',job1),
    # path('job2/',job2),
    path('signup/',signUp),
    path('check/',check),
    path('login/',login),
    path('hashpassword/',hash_all_passwords),
    path('users/',getAllusers),
    path('home/',homerequest,name="home"),
    path('about/',aboutus,name="about"),
    path('welcome/',welcome,name='welcome'),
    path('contact/',contact,name='contact'),
    path('services/',services,name='services'),
    path('projects/',projects,name='projects'),
]
