from django.shortcuts import render
from account.forms import SignupForm
from account.forms import ProfileForm
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
class SignupView(CreateView):

    model = User
    form_class = SignupForm
    template_name = "account/signup.html"



class ProfileView(LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin,DetailView,UpdateView):

    login_url = 'login'
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    context_object_name = "user"
    permission_required = 'account.change_user'

    def test_func(self,*args,**kwargs):
        # print(self.kwargs.get('pk'))
        # print(self.request.user.pk)
        if self.request.user.pk == self.kwargs.get('pk'):

            return True

        else:

            return False
