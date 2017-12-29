from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from.forms import ImageUploadForm
from django.core.mail import send_mail
from django.template import Context
from . import models
from .models import User, Education, WorkExperience, ResearchInterests, Teaching, Students, Publication, Projects, Recognitions, Department, Notifications
from django.db import models
import urllib
import json
import string
import random
import os
# for crawling
import requests
# from bs4 import BeautifulSoup
import html
import re
from bs4 import BeautifulSoup

## FACULTY PORTAL VIEWS START HERE ##


def send_verification_mail(request, webmail, randstr):
    faculty = get_object_or_404(User, webmail=webmail)
    subject = "Faculty Webpage management system mail verification"
    msg = "".join(["Dear ",
                   faculty.name,
                   "\nClick on following link or copy paste in browser to verify webmail and activate your portal",
                   "\nlocalhost:8000/ssl_main/activate_account/",
                   faculty.webmail,
                   "/",
                   randstr])
    send_mail(subject, msg, 'noreply@ssl_main.co', ['mitansh1398@iitg.ernet.in'], fail_silently=False)
    return HttpResponse('Mail Sent')


def send_pass(webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    subject = "Faculty Webpage Management system Forgot Password"
    passwd = faculty.password
    msg = "".join(["Dear ",
                   faculty.name,
                   "\nYour Current password is ",
                   passwd]
                  )
    rec_mail = "".join([webmail, '@iitg.ernet.in'])
    send_mail(subject, msg, 'noreply@ssl_main.co', [rec_mail], fail_silently=False)


def verification_mail(webmail, randstr):
    faculty = get_object_or_404(User, webmail=webmail)
    subject = "Faculty Webpage management system mail verification"
    msg = "".join(["Dear ",
                   faculty.name,
                   "\nClick on following link or copy paste in browser to verify webmail and activate your portal",
                   "\nlocalhost:8000/ssl_main/activate_account/",
                   faculty.webmail,
                   "/",
                   randstr]
                  )
    rec_mail = "".join([webmail, '@iitg.ernet.in'])
    send_mail(subject, msg, 'noreply@ssl_main.co', [rec_mail], fail_silently=False)


def activate_account(request, webmail, randstr):
    faculty = get_object_or_404(User, webmail=webmail, random_string=randstr)
    if faculty.is_active:
        request.session['message'] = 'Account already activated'
        return HttpResponseRedirect('/ssl_main/login/message/')
    else:
        faculty.is_active = True
        faculty.save()
        request.session['message'] = 'Account activated'
        return HttpResponseRedirect('/ssl_main/login/message/')


def loginpage(request):
    if 'faculty_mail' in request.session:
        return HttpResponseRedirect('/ssl_main/portal')
    t = get_template('login/index.html')
    html = t.render({}, request)
    return HttpResponse(html)


def forgotpasspage(request):
    if 'faculty_mail' in request.session:
        return HttpResponseRedirect('/ssl_main/portal')
    t = get_template('login/forgot_pass.html')
    html = t.render({}, request)
    return HttpResponse(html)


def forgotpass(request):
    if 'faculty_mail' in request.session:
        return HttpResponseRedirect('/ssl_main/portal')
    webmail = request.POST['webmail']
    check = User.objects.filter(webmail=webmail).values('password')
    if check.exists():
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            send_pass(webmail)
            request.session['message'] = 'Password has been sent to registered webmail.'
            return HttpResponseRedirect('/ssl_main/login/message/')
        else:
            request.session['message'] = 'Incorrect Response'
            return HttpResponseRedirect('/ssl_main/login/message/')
    else:
        request.session['message'] = 'Wrong Webmail'
        return HttpResponseRedirect('/ssl_main/login/message/')


def signup(request):
    if 'faculty_mail' in request.session:
        return HttpResponseRedirect('/ssl_main/portal')
    name = request.POST['name']
    webmail = request.POST['webmail']
    passwd = request.POST['pass']
    cpasswd = request.POST['cpasswd']
    if passwd != cpasswd:
        t = get_template('login/index.html')
        html = t.render({}, request)
        return HttpResponse(html)
    elif passwd == cpasswd:
        check = User.objects.filter(webmail=webmail)
        if check.exists():
            t = get_template('login/index.html')
            html = t.render({}, request)
            return HttpResponse(html)
        else:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                obj = User(name=name, webmail=webmail, password=passwd, random_string=randstr)
                obj.save()
                verification_mail(webmail, randstr)
                request.session['message'] = 'Activation link has been sent to your webmail. Verify you Webmail to activate your account.'
                return HttpResponseRedirect('/ssl_main/login/message/')
            else:
                t = get_template('login/index.html')
                html = t.render({}, request)
                return HttpResponse(html)


def signin(request):
    if 'faculty_mail' in request.session:
        return HttpResponseRedirect('/ssl_main/portal')
    webmail = request.POST['webmail']
    # request.session['faculty_mail'] = "test15"
    # return HttpResponseRedirect('/ssl_main/portal/')
    check = User.objects.filter(webmail=webmail).values('password')
    if check.exists():
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        passwd = request.POST['password']
        if result['success']:
            if check[0]['password'] == passwd:
                faculty = get_object_or_404(User, webmail=webmail)
                if not faculty.is_active:
                    request.session['message'] = 'Your account is not activated. Click on the link in the mail sent to your registered mail id.'
                    return HttpResponseRedirect('/ssl_main/login/message/')
                request.session['faculty_mail'] = webmail
                return HttpResponseRedirect('/ssl_main/portal/')
            else:
                request.session['message'] = 'Invalid Credentials'
                return HttpResponseRedirect('/ssl_main/login/message/')
        else:
            request.session['message'] = 'Incorrect Response'
            return HttpResponseRedirect('/ssl_main/login/message/')
    else:
        request.session['message'] = 'Invalid Credentials'
        return HttpResponseRedirect('/ssl_main/login/message/')


def updateinfo(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    name = request.POST['name']
    dept = request.POST['dept']
    desg = request.POST['desg']
    resadd = request.POST['resadd']
    resnum = request.POST['resnum']
    offadd = request.POST['offadd']
    offnum = request.POST['offnum']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    faculty.update(
        name=name,
        department=dept,
        designation=desg,
        residence=resadd,
        residence_phone_num=resnum,
        office_room_num=offadd,
        office_phone_ext=offnum,
    )
    return HttpResponseRedirect('/ssl_main/portal/')


def changepass(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    opass = request.POST['opass']
    npass = request.POST['npass']
    cnpass = request.POST['cnpass']
    faculty = User.objects.filter(webmail=request.session['faculty_mail']).values('password')
    if faculty[0]['password'] == opass:
        if cnpass == npass:
            User.objects.filter(webmail=request.session['faculty_mail']).update(password=npass)

    return HttpResponseRedirect('/ssl_main/portal/')


def loginmsg(request):
    return render(request, 'login/message.html', {'message': request.session['message']})


def eduandwork(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    return render(request, 'portal/eduandwork.html', {'user': check})


def researchint(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    return render(request, 'portal/research_int.html', {'user': check})

def mailcrawler(webmail):
    directory = os.path.dirname(os.path.abspath(__file__)) + '/mails/'
    # print(directory)
    for filename in os.listdir(directory):
        exp = open(directory + filename)
        soup = BeautifulSoup(exp, 'lxml')
        text = soup.find('pre')
        text = text.get_text()
        text = text.strip()
        user = get_object_or_404(User, webmail=webmail)
        Pos = user.designation
        u = User.objects.filter(webmail=webmail)
        u.update(designation="Associate Professor")
        if "promotion" in text or "promoted" in text:
            # print("New promotion")
            if "Professor" in text:
                newPos = "Professor"
                if "Assistant" in text and Pos != "Assistant Professor":
                    newPos = "Assistant Professor"
                if "Associate" in text and Pos != "Associate Professor":
                    newPos = "Associate Professor"

                if newPos != Pos:
                    u = User.objects.filter(webmail=webmail)
                    u.update(designation=Pos)
                    # user.designation = newPos
                    # user.save()
                    notifi = "You have been promoted from "+newPos+" to "+Pos
                    obj = Notifications(user=user, description=notifi)
                    obj.save()

        if "awards" in text or 'award' in text:
            strp = text.split("\n")
            for sss in strp:
                if "Title" in sss:
                    title = sss[6:].strip()
                if "Award Name" in sss:
                    award = sss[12:].strip()

            notif = "You have received "+award+" for the publication titled "+title
            obj = Notifications(user=user, description=notif)
            obj.save()

def portal(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    mailcrawler(webmail)
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    notif = Notifications.objects.filter(user=check, seen=False)
    if notif.exists():
        for i in notif:
            i.seen = True
            i.save()
    return render(request, 'portal/index.html', {'user': check, 'notif': notif})


def projects(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    return render(request, 'portal/projects.html', {'user': check})


def publications(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    return render(request, 'portal/publications.html', {'user': check})


def uploadphoto(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    return render(request, 'portal/uploadphoto.html', {'user': check})


def recognitions(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    return render(request, 'portal/recognitions.html', {'user': check})


def teaching(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    return render(request, 'portal/teaching.html', {'user': check})


def students(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    webmail = request.session['faculty_mail']
    check = get_object_or_404(User, webmail=webmail)
    if not check.is_active:
        return HttpResponse('Activte your account first')
    continuing = Students.objects.filter(user=check, status="Continuing")
    completed = Students.objects.filter(user=check, status="Completed")
    return render(request, 'portal/students.html', {'user': check, 'continuing': continuing, 'completed': completed})


def addedu(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    course = request.POST['course']
    institution = request.POST['institution']
    field = request.POST['field']
    start = request.POST['start']
    end = request.POST['end']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Education(course=course, institution=institution, field=field, start_year=start, end_year=end, user=faculty[0])
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/eduandwork/')


def addwork(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    org = request.POST['org']
    start = request.POST['start']
    end = request.POST['end']
    desg = request.POST['desg']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = WorkExperience(organisation=org, start_year=start, end_year=end, designation=desg, user=faculty[0])
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/eduandwork/')


def addinterest(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    interest = request.POST['interest']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = ResearchInterests(research_interests=interest, user=faculty[0])
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/researchinterests/')


def addrecognition(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Recognitions(
            year=request.POST['year'],
            description=request.POST.get('description',''),
            user=faculty[0]
        )
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/recognitions/')


def addteaching(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Teaching(
            user=faculty[0],
            course_code=request.POST['coursenum'],
            course_name=request.POST['coursename'],
            semester=request.POST['semester'],
            session=request.POST['session']
        )
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/teaching/')


def addpublication(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Publication(
            user=faculty[0],
            authors=request.POST['authors'],
            description=request.POST['description'],
            published_year=request.POST['year'],
        )
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/publications/')


def addproject(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    co_pi = request.POST.get('co_pi', 'NA')
    end_year = request.POST.get('end_year', 0)
    if not co_pi:
        co_pi="NA"
    if not end_year:
        end_year=0
    if faculty.exists():
        obj = Projects(
            user=faculty[0],
            project_title=request.POST['project_title'],
            pi=request.POST['pi'],
            co_pi=co_pi,
            status=request.POST['status'],
            funding_agency=request.POST['funding_agency'],
            start_year=request.POST['start_year'],
            end_year=end_year,
        )
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/projects/')


def upload(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.get(webmail=request.session['faculty_mail'])
    if request.method == 'POST':
        img = request.FILES.get('photo', '')
        faculty.img = img
        faculty.save()
    return HttpResponseRedirect('/ssl_main/portal/uploadphoto/')


def addstudent(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    thesis = request.POST['thesis']
    supervisors = request.POST['supervisors']
    if request.POST['status'] == 'Continuing':
        if not thesis:
            thesis = "NA"
        if not supervisors:
            thesis = "NA"
    else:
        if not thesis:
            return HttpResponseRedirect('/ssl_main/portal/students/')
        elif not supervisors:
            return HttpResponseRedirect('/ssl_main/portal/students/')
    if faculty.exists():
        obj = Students(
            user=faculty[0],
            supervisors=supervisors,
            thesis_title=thesis,
            name=request.POST['name'],
            status=request.POST['status'],
            course=request.POST['course'],
        )
        obj.save()
    return HttpResponseRedirect('/ssl_main/portal/students/')


def deleteint(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    val = request.POST['deleteid']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = ResearchInterests.objects.get(id=val)
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/researchinterests/')


def deleteteaching(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Teaching.objects.get(id=request.POST['deleteid'])
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/teaching/')


def deletestudent(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Students.objects.get(id=request.POST['deleteid'])
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/students/')


def deletepublication(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Publication.objects.get(id=request.POST['deleteid'])
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/publications/')


def deleteproject(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Projects.objects.get(id=request.POST['deleteid'])
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/projects/')


def deleterecognition(request):
    if 'faculty_mail' not in request.session:
        return HttpResponseRedirect('/ssl_main/login')
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Recognitions.objects.get(id=request.POST['deleteid'])
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/recognitions/')


def deleteedu(request):
    val = request.POST['deleteid']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = Education.objects.get(id=val)
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/eduandwork/')


def deletework(request):
    val = request.POST['deleteid']
    faculty = User.objects.filter(webmail=request.session['faculty_mail'])
    if faculty.exists():
        obj = WorkExperience.objects.get(id=val)
        obj.delete()
    return HttpResponseRedirect('/ssl_main/portal/eduandwork/')


def logout(request):
    if 'faculty_mail' in request.session:
        del request.session['faculty_mail']
    return HttpResponseRedirect('/ssl_main/login')


## FACULTY WEBPAGE VIEWS START HERE


def fachomepage(request, webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    return render(request, 'facultypage/index.html', {'faculty': faculty})


def facteaching(request, webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    return render(request, 'facultypage/teaching.html', {'faculty': faculty})


def facstudents(request, webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    btechcon = Students.objects.filter(user=faculty, status="Continuing", course="B.Tech")
    btechcom = Students.objects.filter(user=faculty, status="Completed", course="B.Tech")
    mtechcon = Students.objects.filter(user=faculty, status="Continuing", course="M.Tech")
    mtechcom = Students.objects.filter(user=faculty, status="Completed", course="M.Tech")
    phdcon = Students.objects.filter(user=faculty, status="Continuing", course="Ph.D.")
    phdcom = Students.objects.filter(user=faculty, status="Completed", course="Ph.D.")
    return render(request, 'facultypage/student.html', {'faculty': faculty, 'btechcon':btechcon, 'btechcom':btechcom, 'mtechcom':mtechcom, 'mtechcon':mtechcon, 'phdcom':phdcom, 'phdcon':phdcon})


def facprojects(request, webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    return render(request, 'facultypage/projects.html', {'faculty': faculty})


def facpublications(request, webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    return render(request, 'facultypage/publications.html', {'faculty': faculty})


def facrecognitions(request, webmail):
    faculty = get_object_or_404(User, webmail=webmail)
    return render(request, 'facultypage/recognition.html', {'faculty': faculty})


def ssl_main(request):
    return render(request, 'main_site/index.html', {})


def department(request, department_name):
    dept = get_object_or_404(Department, url_code=department_name)
    faculties = User.objects.filter(department=dept.department_name)
    return render(request, 'main_site/departmentpage.html', {'faculties': faculties, 'dept': dept})


##CRAWLING VIEWS

# adding students
def students_crawl(request):
    website = request.POST["url"]
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('div[data-content="3"] div div div div')
    for stud in content:
        name=""
        zzz = stud.find('h4')
        type = str(zzz.get_text()).strip()
        ppp = stud.select('h4 i.icon-gears2')
        qqq = stud.select('h4 i.icon-trophy2')
        if type == 'Ph.D.':
            course = 'Ph.D.'
            if len(ppp) == 1:
                status = 'Continuing'
            else:
                status = 'Completed'
            thesis_title = ""
            supervisors = ""
        elif type == "M.Tech.":
            course = 'M.Tech'
            if len(ppp) == 1:
                status = 'Continuing'
            else:
                status = 'Completed'
            thesis_title = ""
            supervisors = ""
        elif type == "B.Tech.":
            course = 'B.Tech'
            if len(ppp) == 1:
                status = 'Continuing'
            else:
                status = 'Completed'
            thesis_title = ""
            supervisors = ""

        searching = stud.select('ul li')
        for i in searching:
            vpn = str(i.get_text()).split('&diam;')
            counter = 0
            for det in vpn:
                y = det.split(': ')
                if len(y) >= 2:
                    if counter == 0:
                        supervisors = str(y[1]).strip()
                    elif counter == 1:
                        name = str(y[1]).strip()
                    elif counter == 2:
                        thesis_title = str(y[1]).strip()
                else:
                    name = str(y[0]).strip()
                counter = counter + 1
            faculty = get_object_or_404(User, webmail=request.session['faculty_mail'])
            fac_award = Students.objects.filter(user=faculty, name=name, supervisors=supervisors, status=status, thesis_title=thesis_title, course=course)
            if not fac_award.exists():
                obj = Students(user=faculty, name=name, supervisors=supervisors, status=status, thesis_title=thesis_title, course=course)
                obj.save()

    return HttpResponseRedirect('/ssl_main/portal/students/')


# Awards and Recognitions
def awardsandrecog_crawl(request):
    website = request.POST["url"]
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('div[data-content="7"] div div div div ul li p')
    for awards in content:
        prob_year = re.findall('(\d{4})', awards.get_text())
        if len(prob_year) == 1:
            year = prob_year[0]
        else:
            year = 'NA'

        actaward = awards.get_text()
        actaward = actaward.strip()
        faculty = get_object_or_404(User, webmail=request.session['faculty_mail'])
        fac_award = Recognitions.objects.filter(user=faculty, description=actaward, year=year)
        if not fac_award.exists():
            obj = Recognitions(user=faculty, description=actaward, year=year)
            obj.save()

    return HttpResponseRedirect('/ssl_main/portal/recognitions/')


# teaching taken
def course_crawl(request):
    website = request.POST["url"]
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    # return HttpResponse(soup.prettify())
    content = soup.select('div[data-content="2"] div div div div div ul li')
    for total in content:
        ttt = total.get_text()
        sss = ttt.split('&diam;')
        counter = 0
        for strIn in sss:
            if counter == 2:
                a, b = strIn.split(':')
                course_name = b.strip()
                course_code = a.strip()
            elif counter == 1:
                semester = strIn.strip()
            elif counter == 0:
                session = strIn.strip()
            counter = counter + 1
        faculty = get_object_or_404(User, webmail=request.session['faculty_mail'])
        fac_award = Teaching.objects.filter(user=faculty, course_code=course_code, course_name=course_name, session=session, semester=semester)
        if not fac_award.exists():
            obj = Teaching(user=faculty, course_code=course_code, course_name=course_name, session=session, semester=semester)
            obj.save()
            # return HttpResponse("hello")
    return HttpResponseRedirect('ssl_main/portal/teaching')


# adding projects
def projects_crawl(request):
    website = request.POST["url"]
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('div[data-content="4"] div div div div p')
    for project in content:
        project_title = project.find(text='Project Title:')
        pi = project.find(text='PI:')
        funding_agency = project.find(text='Funding Agency:')
        start_year = project.find(text='Start Year:')
        end_year = project.find(text='End Year:')
        co_pi = project.find(text='Co-PI:')
        status = 'Completed'

        if end_year == None :
            end_year = ""
            status = 'ongoing'
            project_title = str(project_title.next).strip()
            pi = str(pi.next).strip()
            funding_agency = str(funding_agency.next).strip()
            start_year = str(start_year.next).strip()
            start_year = start_year[:4]
        else:
            end_year = str(end_year.next).strip()
            project_title = str(project_title.next).strip()
            pi = str(pi.next).strip()
            funding_agency = str(funding_agency.next).strip()
            start_year = str(start_year.next).strip()
            start_year = start_year[:4]

        if co_pi == None:
            co_pi = 'None'
        else:
            co_pi = str(co_pi.next).strip()
        faculty = get_object_or_404(User, webmail=request.session['faculty_mail'])
        fac_award = Projects.objects.filter(user=faculty, pi=pi, project_title=project_title, funding_agency=funding_agency, co_pi=co_pi, start_year=start_year, end_year=end_year, status=status)
        if not fac_award.exists():
            obj = Projects(user=faculty, pi=pi, project_title=project_title, funding_agency=funding_agency, co_pi=co_pi, start_year=start_year, end_year=end_year, status=status)
            obj.save()

    return HttpResponseRedirect('/ssl_main/portal/projects/')


# publications
def publication_crawl(request):
    website = request.POST["url"]
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('div[data-content="5"] div div div div ul li p')
    for publi in content:
        prob_year = re.findall('(\d{4})', publi.get_text())
        size = len(prob_year)
        if size > 0:
            year = prob_year[size-1]
        else:
            year = 'NA'
        pre = publi.get_text()
        authors, description = pre.split(', "', 1)
        description = '"' + description
        faculty = get_object_or_404(User, webmail=request.session['faculty_mail'])
        fac_award = Publication.objects.filter(user=faculty, authors=authors, description=description, published_year=year)
        if not fac_award.exists():
            obj = Publication(user=faculty, authors=authors, description=description, published_year=year)
            obj.save()

    return HttpResponseRedirect('/ssl_main/portal/publications/')
