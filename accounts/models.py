from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django_countries.fields import CountryField

# Create your models here.

class Profile(models.Model):
    JOB_STATUS = (
        ('Employed', 'Employed'),
        ('Student', 'Student'),
        ('Unemployed', 'Unemployed'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    job_status = models.CharField(max_length=10, choices=JOB_STATUS, blank=True, null=True)
    date_birth = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar/default.jpg')
        return avatar
    
    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name

