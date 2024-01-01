import datetime
from django.contrib import messages
from django.db.models import Sum, F
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from apps.admin_panel import models as domains
from apps.site.forms.contact import CreateContactForm
from django.utils.translation import gettext_lazy as _


# region home

def home_page(request: HttpRequest):
    context = {
        'articles': domains.Article.objects.filter(is_delete=False, publish_date__lte=datetime.datetime.now(), is_active=True).order_by('-id')[:3],
        'courses': domains.Course.objects.prefetch_related('main_master', 'main_master__user').annotate(total_section_duration=Sum(F('coursesection__duration__hour') * 60 + F('coursesection__duration__minute'))).order_by('-id')[:9],
        'categories': domains.CourseCategory.objects.filter(is_active=True).exclude(is_delete=True).order_by('-id')[:9]
    }

    return render(request, 'site/home/index.html', context)


# endregion

# region contact us

class ContactView(View):
    def get(self, request: HttpRequest):
        form = CreateContactForm()
        site_setting: domains.SiteSetting = domains.SiteSetting.objects.first()
        return render(request, 'site/home/contact_us.html', {
            'form': form,
            'site_setting': site_setting
        })

    def post(self, request: HttpRequest):
        form = CreateContactForm(request.POST)
        if form.is_valid():
            new_contact = domains.ContactUs(
                subject=form.cleaned_data.get('subject'),
                text=form.cleaned_data.get('text'),
                full_name=form.cleaned_data.get('full_name'),
                email=form.cleaned_data.get('email'),
                is_seen=False
            )
            new_contact.save()
            messages.add_message(request, messages.SUCCESS, _('Your message has been send successfully'))
            return redirect(reverse('contact_us_page'))
        else:
            messages.add_message(request, messages.ERROR, _('An error occurred'))

        site_setting: domains.SiteSetting = domains.SiteSetting.objects.first()
        return render(request, 'site/home/contact_us.html', {
            'form': form,
            'site_setting': site_setting
        })


# endregion

# region about us

def about_us_view(request: HttpRequest):
    site_setting: domains.SiteSetting = domains.SiteSetting.objects.first()
    return render(request, 'site/home/about_us.html', {
        'site_setting': site_setting
    })


# endregion

# region dynamic page view

def dynamic_page(request: HttpRequest, url_title: str):
    page = domains.DynamicPage.objects.get_page_by_url_title(url_title)
    if page is None:
        raise Http404(_('Information not found'))

    return render(request, 'site/home/page.html', {
        'page': page
    })

# endregion
