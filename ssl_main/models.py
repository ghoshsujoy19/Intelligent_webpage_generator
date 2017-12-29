from django.db import models


class User(models.Model):
    webmail = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)

    department_choices = {
        ('Computer Science and Engineering', 'Computer Science and Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Electronics and Electrical Engineering', 'Electronics and Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Bio-Tech', 'Bio-Tech'),
        ('Chemical Engineering','Chemical Engineering'),
        ('Chemistry', 'Chemistry'),
        ('Design', 'Design'),
        ('Physics' ,'Physics'),
        ('Humanities', 'Humanities'),
    }

    department = models.CharField(
        max_length=200,
        default='',
        choices=department_choices,
    )
    designation_choice = {
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Head of Department', 'Head of Department'),
    }

    designation = models.CharField(
        max_length=50,
        choices=designation_choice,
        default=''
    )

    is_active = models.BooleanField(default=False)
    office_room_num = models.CharField(max_length=20, default='')
    office_phone_ext = models.BigIntegerField(default=0)
    password = models.CharField(max_length=200)

    residence = models.CharField(max_length=500, default='')
    residence_phone_num = models.BigIntegerField(default=0)
    img = models.ImageField(upload_to='static/faculty_img', default="static/faculty_img/find_user.png")

    webpage_published = models.BooleanField(default=False)
    random_string = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=200, default="")
    field = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        strn = self.user.name + self.course
        return strn


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return self.organisation


class ResearchInterests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    research_interests = models.CharField(max_length=200)

    def __str__(self):
        return self.research_interests


class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status_choice = {
        ('Continuing', 'Continuing'),
        ('Completed', 'Completed'),
    }
    status = models.CharField(
        max_length=200,
        choices=status_choice
    )
    course_choice = {
        ('B.Tech', 'B.Tech'),
        ('M.Tech', 'M.Tech'),
        ('Ph.D.', 'Ph.D.'),
    }
    course = models.CharField(
        max_length=200,
        choices=course_choice,
    )
    thesis_title = models.CharField(max_length=200, default="   ")
    supervisors = models.CharField(max_length=200, default="")


class Recognitions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    year = models.CharField(max_length=200, default="")


class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    pi = models.CharField(max_length=200)
    co_pi = models.CharField(max_length=200)
    funding_agency = models.CharField(max_length=200)
    start_year = models.CharField(max_length=200, default="")
    end_year = models.CharField(max_length=200, default="")
    status_choice = {
        ('ongoing', '0'),
        ('Completed', '1'),
    }
    status = models.CharField(
        max_length=200,
        choices=status_choice
    )


class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authors = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    published_year = models.CharField(max_length=200, default="")


class DeptResponsibilities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    desg = models.CharField(max_length=200)


class Teaching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    semester_choices = {
        ('Odd Semester', 'Odd Semester'),
        ('Even Semester', 'Even Semester'),
    }
    session = models.CharField(max_length=200)
    semester = models.CharField(
        choices=semester_choices,
        max_length=200,
        default='Odd Semester'
    )


class Department(models.Model):
    department_choices = {
        ('Computer Science and Engineering', 'Computer Science and Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Electronics and Electrical Engineering', 'Electronics and Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Bio-Tech', 'Bio-Tech'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Chemistry', 'Chemistry'),
        ('Design', 'Design'),
        ('Physics', 'Physics'),
        ('Humanities', 'Humanities')
    }

    department_name = models.CharField(
        max_length=200,
        choices=department_choices,
    )
    url_code = models.CharField(max_length=200)

    def __str__(self):
        return self.department_name


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, default="")