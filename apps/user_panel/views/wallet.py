from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from apps.admin_panel.models import UserWallet
from django.utils.translation import get_language
from apps.user_panel.forms.wallet import ChargeWalletForm
from django.utils.translation import gettext_lazy as _
from utilities.web.http import get_client_ip


# region user wallets list

@method_decorator(login_required, name='dispatch')
class UserWalletListView(View):
    def get(self, request: HttpRequest):
        query, filter_items = UserWallet.objects.filter_wallets(
            user_id=request.user.id,
            start_date=request.GET.get('start_date') or '',
            end_date=request.GET.get('end_date') or '',
            is_paid_check_list=[True]
        )

        paginator = Paginator(query, 10)
        page_obj: Page = paginator.get_page(request.GET.get('page'))
        context = {
            'filter_items': filter_items,
            'paginator': paginator,
            'page_obj': page_obj,
            'current_language': get_language()
        }
        return render(request, 'user_panel/wallets/user_wallets.html', context)


# endregion

# region charge wallet

@method_decorator(login_required, name='dispatch')
class ChargeWalletView(View):
    def get(self, request: HttpRequest):
        charge_form = ChargeWalletForm()
        context = {
            'form': charge_form
        }
        return render(request, 'user_panel/wallets/charge_wallet.html', context)

    def post(self, request: HttpRequest):
        charge_form = ChargeWalletForm(request.POST)
        if charge_form.is_valid():
            UserWallet.objects.charge_user_wallet(request.user.id, charge_form.cleaned_data.get('price'), get_client_ip(request))
            messages.add_message(request, messages.SUCCESS, _('Your wallet has been charged'))
            # todo: send user to bank
            return redirect(reverse('user_wallets_page'))
        else:
            messages.add_message(request, messages.ERROR, _('An error occurred'))

        context = {
            'form': charge_form
        }
        return render(request, 'user_panel/wallets/charge_wallet.html', context)

# endregion
