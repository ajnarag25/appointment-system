from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class depts(AbstractUser):
    admintype = [
        ('OAA','Office of Academic Affairs'),
        ('DIT','Department of Information Technology'),
        ('DLA','Department of Liberal Arts'),
        ('OCL','Office of Campus Library'),
        ('ORE','Office of Research and Extension'),
        ('DMS','Department of Mathematics and Science'),
        ('DOE','Department of Engineering'),
        ('OSA','Office of Student Affairs'),
        ('UITC','University Information Technology Center'),
        ('DPE','Department of Physical Education'),
        ('SD','Security Department'),
    ]
    
    department = models.CharField(max_length=200, choices = admintype, verbose_name = 'department')

class appointmentForm(models.Model):
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    yrlevel = models.IntegerField()
    yrgraduate = models.IntegerField()
    studentnum = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    contactperson = models.CharField(max_length=100)
    pdate = models.CharField(max_length=100)
    ptime = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    status = models.CharField(max_length=100) 
    notes = models.CharField(max_length=100)
    user = models.CharField(max_length=100)