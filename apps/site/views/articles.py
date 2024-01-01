import datetime
from django.contrib import messages
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.list import ListView
from apps.admin_panel import models as domains
from apps.site.forms.article import AddArticleCommentForm


# region articles list

class ArticlesPage(ListView):
    model = domains.Article
    paginate_by = 6
    template_name = 'site/articles/articles_list.html'

    def get_queryset(self):
        query = domains.Article.objects.filter(is_delete=False, publish_date__lte=datetime.datetime.now(), is_active=True)
        return query


# endregion

# region article short link

def article_short_link(request: HttpRequest, article_id):
    article = domains.Article.objects.get_by_id(article_id)
    if article is not None and article.is_active and not article.is_delete:
        return redirect(article.get_article_detail_url(), permanent=True)

    raise Http404(_('Information not found'))


# endregion

# region article detail

class ArticleDetailPage(View):
    def get(self, request: HttpRequest, article_id, article_title):
        article: domains.Article = domains.Article.objects.get_article_for_show(article_id)
        if article is None:
            raise Http404(_('Information not found'))

        article.visit_count += 1
        article.save()

        comments = domains.ArticleComment.objects.get_article_comments_for_show(article_id)

        context = {
            'article': article,
            'comments': comments,
            'comments_count': domains.ArticleComment.objects.get_article_total_comments_count(article_id),
            'comment_form': AddArticleCommentForm(),
            'current_domain': request.META['HTTP_HOST']
        }
        return render(request, 'site/articles/article_detail.html', context)


# endregion

# region add comment

class AddArticleCommentPage(View):
    def post(self, request: HttpRequest, article_id):
        add_comment_form = AddArticleCommentForm(request.POST)
        article = domains.Article.objects.get_by_id(article_id)
        if add_comment_form.is_valid():
            if article is not None:
                if article.can_add_comment:
                    parent_comment = domains.ArticleComment.objects.get_by_id(add_comment_form.cleaned_data.get('parent_id'))
                    comment = domains.ArticleComment(
                        article_id=article_id,
                        text=add_comment_form.cleaned_data.get('text'),
                        sender_id=request.user.id,
                        comment_state=domains.ArticleComment.ArticleCommentState.NOT_SEEN,
                        parent=parent_comment
                    )
                    comment.save()
                    messages.add_message(request, messages.SUCCESS, _('Your comment will be displayed after review'))
                else:
                    messages.add_message(request, messages.ERROR, _('Can not add comment for this article'))
            else:
                messages.add_message(request, messages.ERROR, _('Information not found'))
        else:
            messages.add_message(request, messages.ERROR, _('Please enter comment text'))

        return redirect(article.get_article_detail_url())

# endregion
