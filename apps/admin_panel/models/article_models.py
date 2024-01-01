import datetime
from django.db import models
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


# region article

class ArticleManager(models.Manager):
    def get_article_for_show(self, article_id):
        return self.get_queryset() \
            .prefetch_related('articlecomment_set', 'author') \
            .filter(id=article_id, is_active=True, publish_date__lte=datetime.datetime.now()).first()

    def get_by_id(self, article_id):
        return self.get_queryset().filter(id=article_id).first()


class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=_('Title'))
    slug = models.SlugField(max_length=300, unique=True, verbose_name=_('Article slug field'))
    short_description = models.CharField(max_length=200, verbose_name=_('Short description'))
    text = RichTextField(verbose_name=_('Text'))
    image = models.ImageField(upload_to='images/article', max_length=300, verbose_name=_('Image'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    publish_date = models.DateTimeField(verbose_name=_('Publish date'))
    visit_count = models.IntegerField(verbose_name=_('Visit count'), default=0)
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('Author'))
    related_articles = models.ManyToManyField('Article', blank=True, verbose_name=_('Related articles'))
    is_delete = models.BooleanField(verbose_name=_('Is deleted'), default=False)
    can_add_comment = models.BooleanField(verbose_name=_('Can add comment'), default=True)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_article_detail_url(self):
        return reverse('articles_detail_page', kwargs={'article_id': self.id, 'article_title': self.title.lower().replace(' ', '-')})

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


# endregion

# region article comment

class ArticleCommentsManager(models.Manager):
    def get_by_id(self, comment_id):
        return self.get_queryset().filter(id=comment_id).first()

    def get_article_comments_for_show(self, article_id):
        return self.get_queryset() \
            .order_by('-create_date') \
            .filter(article_id=article_id, is_delete=False, comment_state=ArticleComment.ArticleCommentState.ACCEPTED, parent_id__isnull=True) \
            .prefetch_related(Prefetch('articlecomment_set', queryset=ArticleComment.objects.filter(is_delete=False, comment_state=ArticleComment.ArticleCommentState.ACCEPTED)))

    def get_article_total_comments_count(self, article_id):
        return self.get_queryset() \
            .filter(article_id=article_id, is_delete=False, comment_state=ArticleComment.ArticleCommentState.ACCEPTED).count()


class ArticleComment(models.Model):
    class ArticleCommentState(models.TextChoices):
        NOT_SEEN = 'NotSeen', _('Not seen')
        ACCEPTED = 'Accepted', _('Accepted')
        NOT_ACCEPTED = 'NotAccepted', _('Not accepted')

    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name=_('Article'))
    sender = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('Sender'))
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Parent comment'))
    text = RichTextField(verbose_name=_('Text'))
    comment_state = models.CharField(max_length=200, choices=ArticleCommentState.choices, default=ArticleCommentState.NOT_SEEN, verbose_name=_('Comment state'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Is deleted'))

    objects = ArticleCommentsManager()

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = _('Article comment')
        verbose_name_plural = _('Article comments')


# endregion

