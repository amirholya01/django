from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from apps.admin_panel.models import User, Ticket, UserWallet
from apps.user_panel.forms.account import ChangePasswordForm, ChangeUserInfoForm


# region dashboard

@method_decorator(login_required, name='dispatch')
class UserDashboardPage(View):
    def get(self, request: HttpRequest):
        context = {
            'tickets_count': Ticket.objects.get_user_tickets_count(request.user.id),
            'paid_transactions_count': UserWallet.objects.get_user_paid_transactions_count(request.user.id)
        }
        return render(request, 'user_panel/account/index.html', context)


# endregion

# region change password

@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        change_pass_form = ChangePasswordForm()
        return render(request, 'user_panel/account/change_password.html', {
            'form': change_pass_form
        })

    def post(self, request: HttpRequest):
        change_pass_form = ChangePasswordForm(request.POST)
        if change_pass_form.is_valid():
            user: User = User.objects.get_user_by_id(request.user.id)
            if user.check_password(change_pass_form.cleaned_data.get('current_password')):
                user.set_password(change_pass_form.cleaned_data.get('password'))
                user.save()
                logout(request)
                messages.add_message(request, messages.SUCCESS, _('Your password has been successfully edited'))
                return redirect(reverse('login_page'))
            else:
                messages.add_message(request, messages.ERROR, _('Your current password is incorrect'))
        return render(request, 'user_panel/account/change_password.html', {
            'form': change_pass_form
        })


# endregion

# region change user information

@method_decorator(login_required, name='dispatch')
class ChangeUserInfoPage(View):
    def get(self, request: HttpRequest):
        user: User = User.objects.get_user_by_id(request.user.id)
        change_info_form = ChangeUserInfoForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name
        })
        return render(request, 'user_panel/account/change_user_info.html', {'form': change_info_form})

    def post(self, request: HttpRequest):
        change_info_form = ChangeUserInfoForm(request.POST)
        if change_info_form.is_valid():
            user: User = User.objects.get_user_by_id(request.user.id)
            user.first_name = change_info_form.cleaned_data.get('first_name')
            user.last_name = change_info_form.cleaned_data.get('last_name')
            user.save()
            messages.add_message(request, messages.SUCCESS, _('Your information has been successfully edited'))
        else:
            change_info_form.add_error('first_name', _('An error occurred'))
        return render(request, 'user_panel/account/change_user_info.html', {'form': change_info_form})

# endregion
