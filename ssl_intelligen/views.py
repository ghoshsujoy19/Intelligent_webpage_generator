from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template import Context
from django.db import models
import urllib
import json
import string
import random

def loginpage(request):
    t = get_template('login2/index.html')
    html = t.render()
    return HttpResponse(html)

# def signup(request):
#     message = "ghoshsujoy19@gmail.com"
# 	if 'email' in request.POST:
# 		nm = "%s" % request.POST['email']
# 		if nm != message:
# 			return loginpage(request, True)
#
# 	if 'password' in request.POST:
# 		message += " %s" % request.POST['password']
# 	#loginpage(request)
# 	return HttpResponse(message)
#


def sendmail(request):
    send_mail(
        subject='This is subject',
        message='This will be the body\n End line is possible',
        from_email='minshu1398@gmail.com',
        recipient_list=['minshu.jain@gmail.com'],
        fail_silently=False,
    )
    msg = 'Mail Sent!!!'
    return HttpResponse(msg)


def ssl_main(request):
    return render(request, 'main_site/index.html', {})


def department(request, department_name):
    return render(request, 'main_site/departmentpage.html', {'department': department_name})