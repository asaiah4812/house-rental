from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2' ]

class ProfileUpdate(ModelForm):
    class Meta:
        model = Profile
        fields = ['realname', 'email', 'phone', 'job_status', 'image', 'date_birth', 'bio', 'country', 'city']
