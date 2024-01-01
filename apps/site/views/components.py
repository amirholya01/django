from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render
from apps.admin_panel import models as domains


# region layout

def site_header(request: HttpRequest):
    site_setting: domains.SiteSetting = domains.SiteSetting.objects.first()
    links = domains.DynamicLink.objects.get_active_links_by_position(domains.DynamicLink.LinkPosition.SITE_HEADER)
    context = {
        'links': links,
        'site_setting': site_setting
    }
    return render(request, 'site/components/site_header.html', context)


def site_footer(request: HttpRequest):
    site_setting: domains.SiteSetting = domains.SiteSetting.objects.first()
    links = domains.DynamicLink.objects.get_active_links_by_position(domains.DynamicLink.LinkPosition.SITE_FOOTER)
    context = {
        'links': links,
        'settings': site_setting
    }
    return render(request, 'site/components/site_footer.html', context)


# endregion

# region auth

def auth_description(request: HttpRequest):
    return render(request, 'site/components/auth_description.html')


# endregion

# region articles

def article_categories(request: HttpRequest):
    categories = domains.ArticleCategory.objects.annotate(Count('article')).filter(is_delete=False)
    return render(request, 'site/components/article_categories.html', {
        'categories': categories
    })


def article_most_visited(request: HttpRequest):
    return render(request, 'site/components/article_most_visit.html', {
        'articles': domains.Article.objects.order_by('-visit_count')[:10]
    })

# endregion
