from django.urls import path
from account.views import SignupView
from account.views import ProfileView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView




urlpatterns = [
    path("signup",SignupView.as_view(),name = 'signup'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name="account/password_reset_form.html",
                                                      email_template_name="account/password_reset_email.html"), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name="account/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="account/password_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name="account/password_reset_complete.html"), name='password_reset_complete'),
    path('password_change/', PasswordChangeView.as_view(
        template_name="account/password_change_form.html"), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name="account/password_change_done.html"), name='password_change_done'),
    path('profile/<int:pk>',ProfileView.as_view(),name='profile'),
    
    
]