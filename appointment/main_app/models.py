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
