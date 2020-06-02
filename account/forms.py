from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):

    contact = forms.RegexField(regex="^[6-9][0-9]{9}$",error_messages={"invalid":"please provide valid phone number"},required=False)

    
    class Meta:

        model = User
        fields = ("username","role","password1","password2","email",'contact')


class ProfileForm(forms.ModelForm):

    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # contact = forms.RegexField(regex="^[6-9][0-9]{9}$",error_messages={"invalid":"please provide valid phone number"},required=False)

    class Meta:

        model = User
        fields = ['first_name',"last_name",'age','gender','bio','email','contact','address','image']