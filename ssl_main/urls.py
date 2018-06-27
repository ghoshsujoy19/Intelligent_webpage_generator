"""intelligen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('', views.ssl_main, name="main"),
    path('dept/', views.ssl_main),
    path('dept/<str:department_name>/', views.department, name="dept"),
    path('login/', views.loginpage, name="login"),
    path('login/message/', views.loginmsg, name="loginmsg"),
    path('forgotpass/', views.forgotpasspage, name="forgotpass"),
    path('sendpass/', views.forgotpass),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup),
    path('signin/', views.signin),
    path('portal/', views.portal, name="portal"),
    path('portal/uploadphoto/', views.uploadphoto, name="uploadphoto"),
    path('portal/researchinterests/', views.researchint, name="researchinterests"),
    path('portal/eduandwork/', views.eduandwork, name="eduandwork"),
    path('portal/teaching/', views.teaching, name="teaching"),
    path('portal/students/', views.students, name="students"),
    path('portal/publications/', views.publications, name="publications"),
    path('portal/projects/', views.projects, name="projects"),
    path('portal/recognitions/', views.recognitions, name="recognitions"),
    path('upload/', views.upload),
    path('updateinfo/', views.updateinfo),
    path('changepass/', views.changepass),
    path('addedu/', views.addedu),
    path('addwork/', views.addwork),
    path('addinterest/', views.addinterest),
    path('addteaching/', views.addteaching),
    path('addstudent/', views.addstudent),
    path('addrecognition/', views.addrecognition),
    path('addpublication/', views.addpublication),
    path('addproject/', views.addproject),
    path('deleteint/', views.deleteint),
    path('deleteteaching/', views.deleteteaching),
    path('deleteedu/', views.deleteedu),
    path('deletework/', views.deletework),
    path('deletestudent/', views.deletestudent),
    path('deletepublication/', views.deletepublication),
    path('deleteproject/', views.deleteproject),
    path('deleterecognition/', views.deleterecognition),
    path('facultypage/<str:webmail>/', views.fachomepage, name="home"),
    path('facultypage/<str:webmail>/teaching/', views.facteaching, name="facteaching"),
    path('facultypage/<str:webmail>/students/', views.facstudents, name="facstudents"),
    path('facultypage/<str:webmail>/projects/', views.facprojects, name="facprojects"),
    path('facultypage/<str:webmail>/publications/', views.facpublications, name="facpublications"),
    path('facultypage/<str:webmail>/recognition/', views.facrecognitions, name="facrecognitions"),
    path('verifymail/<str:webmail>/<str:randstr>/', views.send_verification_mail),
    path('activate_account/<str:webmail>/<str:randstr>/', views.activate_account),

    path('project_crawl/', views.projects_crawl),
    path('publication_crawl/', views.publication_crawl),
    path('students_crawl/', views.students_crawl),
    path('recog_crawl/', views.awardsandrecog_crawl),
    path('teaching_crawl/', views.course_crawl),
]
