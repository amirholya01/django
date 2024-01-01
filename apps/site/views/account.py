import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from apps.admin_panel import models as domains
from apps.site.forms.account import ResetPasswordForm, ForgotPassword, LoginForm, RegisterForm
from utilities.decorators.auth_decorators import redirect_if_logged_in
from utilities.senders.email_sender import send_email


# region register

class RegisterPage(View):
    @method_decorator(redirect_if_logged_in())
    def get(self, request: HttpRequest):
        register_form = RegisterForm()
        return render(request, 'site/account/register.html', {
            'form': register_form
        })

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # check user is not exists
            if not domains.User.objects.is_exists_user_by_email(register_form.cleaned_data.get('email')):
                # create user
                new_user = domains.User(
                    email=register_form.cleaned_data.get('email'),
                    is_active=False,
                    email_active_code=get_random_string(100),
                    username=register_form.cleaned_data.get('email')
                )
                new_user.set_password(register_form.cleaned_data.get('password'))
                new_user.save()
                site_setting = domains.SiteSetting.objects.first()
                send_email(_('Active account'), [new_user.email], {
                    'user': new_user,
                    'site_setting': site_setting
                }, 'emails/register.html')
                messages.add_message(request, messages.SUCCESS, _('You have successfully registered'))
                messages.add_message(request, messages.INFO, _('An email containing an activation link has been sent to you'))
                return redirect(reverse('login_page'))
            else:
                register_form.add_error('email', _('This email is used by another user'))

        return render(request, 'site/account/register.html', {
            'form': register_form
        })


# endregion

# region login

class LoginPage(View):
    @method_decorator(redirect_if_logged_in())
    def get(self, request: HttpRequest):
        login_form = LoginForm()
        return render(request, 'site/account/login.html', {
            'form': login_form
        })

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # get user by email
            user = domains.User.objects.get_user_by_email(login_form.cleaned_data.get('email'))
            if user is not None:
                if user.is_active:
                    # check user password
                    if user.check_password(login_form.cleaned_data.get('password')):
                        login(request, user)
                        messages.add_message(request, messages.SUCCESS, _('Welcome'))
                        if user.is_superuser:
                            return redirect('/admin/')
                        return redirect(reverse('user_dashboard_page'))
                    else:
                        login_form.add_error('email', _('User not found'))
                else:
                    login_form.add_error('email', _('Your account is not activated'))
            else:
                login_form.add_error('email', _('User not found'))
        return render(request, 'site/account/login.html', {
            'form': login_form
        })


# endregion

# region activate admin_account

class ActivateAccountPage(View):
    @method_decorator(redirect_if_logged_in())
    def get(self, request, email_active_code):
        # get user by email active code
        user = domains.User.objects.get_user_by_email_active_code(email_active_code)
        if user is not None:
            # activate user admin_account and change email active code again
            user.is_active = True
            user.email_active_code = get_random_string(100)
            user.date_joined = datetime.datetime.now()
            user.save()
            messages.add_message(request, messages.SUCCESS, _('Your account is successfully activated'))
            return redirect(reverse('login_page'))
        else:
            raise Http404(_('Information not found'))


# endregion

# region forgot password

class ForgotPasswordPage(View):
    @method_decorator(redirect_if_logged_in())
    def get(self, request: HttpRequest):
        register_form = ForgotPassword()
        return render(request, 'site/account/forgot_pass.html', {
            'form': register_form
        })

    def post(self, request: HttpRequest):
        register_form = ForgotPassword(request.POST)
        if register_form.is_valid():
            # get user by email
            user: domains.User = domains.User.objects.get_user_by_email(register_form.cleaned_data.get('email'))
            if user is not None:
                # send reset password email
                site_setting: domains.SiteSetting = domains.SiteSetting.objects.first()
                send_email(_('Reset password'), [user.email], {
                    'user': user,
                    'site_setting': site_setting
                }, 'emails/reset_pass.html')
                return redirect(reverse('login_page'))
            else:
                register_form.add_error('email', _('User not found'))

        return render(request, 'site/account/forgot_pass.html', {
            'form': register_form
        })


# endregion

# region reset password

class ResetPasswordPage(View):
    @method_decorator(redirect_if_logged_in())
    def get(self, request: HttpRequest, email_active_code: str):
        # check user is exists or not
        user: domains.User = domains.User.objects.get_user_by_email_active_code(email_active_code)
        if user is None:
            raise Http404(_('User not found'))
        reset_pass_form = ResetPasswordForm(initial={'email_active_code': user.email_active_code})
        return render(request, 'site/account/reset_password.html', {
            'form': reset_pass_form
        })

    def post(self, request: HttpRequest, email_active_code: str):
        reset_pass_form = ResetPasswordForm(request.POST)
        if reset_pass_form.is_valid():
            # check user is exists or not
            user: domains.User = domains.User.objects.get_user_by_email_active_code(email_active_code)
            if user is None:
                raise Http404(_('User not found'))
            else:
                user.set_password(reset_pass_form.cleaned_data.get('password'))
                user.email_active_code = get_random_string(100)
                user.save()
                messages.add_message(request, messages.SUCCESS, _('Your password has been changed successfully'))
                return redirect(reverse('login_page'))

        return render(request, 'site/account/forgot_pass.html', {
            'form': reset_pass_form
        })


# endregion

# region logout

class LogoutPage(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse('login_page'))
        else:
            return redirect(reverse('home_page'))

# endregion
