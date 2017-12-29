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


urlpatterns = [
    url(r'^$', views.ssl_main, name="main"),
    url(r'^dept/$', views.ssl_main),
    url(r'dept/(?P<department_name>\w+)/$', views.department, name="dept"),
    url(r'login/$', views.loginpage, name="login"),
    url(r'login/message/$', views.loginmsg, name="loginmsg"),
    url(r'forgotpass/$', views.forgotpasspage, name="forgotpass"),
    url(r'sendpass/$', views.forgotpass),
    url(r'logout/$', views.logout, name="logout"),
    url(r'signup/$', views.signup),
    url(r'signin/', views.signin),
    url(r'portal/$', views.portal, name="portal"),
    url(r'portal/uploadphoto/$', views.uploadphoto, name="uploadphoto"),
    url(r'portal/researchinterests/$', views.researchint, name="researchinterests"),
    url(r'portal/eduandwork/$', views.eduandwork, name="eduandwork"),
    url(r'portal/teaching/$', views.teaching, name="teaching"),
    url(r'portal/students/$', views.students, name="students"),
    url(r'portal/publications/$', views.publications, name="publications"),
    url(r'portal/projects/$', views.projects, name="projects"),
    url(r'portal/recognitions/$', views.recognitions, name="recognitions"),
    url(r'upload/$', views.upload),
    url(r'updateinfo/$', views.updateinfo),
    url(r'changepass/$', views.changepass),
    url(r'addedu/$', views.addedu),
    url(r'addwork/$', views.addwork),
    url(r'addinterest/$', views.addinterest),
    url(r'addteaching/$', views.addteaching),
    url(r'addstudent/$', views.addstudent),
    url(r'addrecognition/$', views.addrecognition),
    url(r'addpublication/$', views.addpublication),
    url(r'addproject/$', views.addproject),
    url(r'deleteint/$', views.deleteint),
    url(r'deleteteaching/$', views.deleteteaching),
    url(r'deleteedu/$', views.deleteedu),
    url(r'deletework/$', views.deletework),
    url(r'deletestudent/$', views.deletestudent),
    url(r'deletepublication/$', views.deletepublication),
    url(r'deleteproject/$', views.deleteproject),
    url(r'deleterecognition/$', views.deleterecognition),
    url(r'facultypage/(?P<webmail>\w+)/$', views.fachomepage, name="home"),
    url(r'facultypage/(?P<webmail>\w+)/teaching/$', views.facteaching, name="facteaching"),
    url(r'facultypage/(?P<webmail>\w+)/students/$', views.facstudents, name="facstudents"),
    url(r'facultypage/(?P<webmail>\w+)/projects/$', views.facprojects, name="facprojects"),
    url(r'facultypage/(?P<webmail>\w+)/publications/$', views.facpublications, name="facpublications"),
    url(r'facultypage/(?P<webmail>\w+)/recognition/$', views.facrecognitions, name="facrecognitions"),
    url(r'verifymail/(?P<webmail>\w+)/(?P<randstr>\w+)/$', views.send_verification_mail),
    url(r'activate_account/(?P<webmail>\w+)/(?P<randstr>\w+)/$', views.activate_account),

    url(r'project_crawl/$', views.projects_crawl),
    url(r'publication_crawl/$', views.publication_crawl),
    url(r'students_crawl/$', views.students_crawl),
    url(r'recog_crawl/$', views.awardsandrecog_crawl),
    url(r'teaching_crawl/$', views.course_crawl),
]
