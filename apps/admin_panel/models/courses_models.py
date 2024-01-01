import os
import datetime
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Prefetch, Count, Q, Sum, F
from django.db.models.functions import Cast
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


# region course category

class CourseCategoryManager(models.Manager):
    def get_all_active_categories_with_sub_categories(self):
        return self.get_queryset().filter(is_active=True, parent_id__isnull=True) \
            .prefetch_related(Prefetch('coursecategory_set', queryset=CourseCategory.objects.filter(is_active=True).annotate(courses_count=Count('course')))) \
            .annotate(courses_count=Count('course'))


class CourseCategory(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Title'))
    url_title = models.CharField(max_length=200, unique=True, verbose_name=_('Url title'))
    icon_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Icon name'))
    image = models.ImageField(upload_to='images/course-category', null=True, blank=True, verbose_name=_('Image'))
    short_description = models.CharField(max_length=1000, verbose_name=_('Short description'))
    description = RichTextField(null=True, blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    parent = models.ForeignKey('CourseCategory', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Parent'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Is deleted'))

    objects = CourseCategoryManager()

    def __str__(self):
        return f'{self.title} / {self.url_title}'

    class Meta:
        verbose_name = _('Course category')
        verbose_name_plural = _('Course categories')


# endregion

# region course level

class CourseLevelManager(models.Manager):
    def get_all_levels_by_order(self):
        return self.get_queryset().annotate(courses_count=Count('course')).order_by('order')


class CourseLevel(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    url_title = models.CharField(max_length=200, verbose_name=_('Url title'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    objects = CourseLevelManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Course level')
        verbose_name_plural = _('Course levels')


# endregion

# region course

class CourseManager(models.Manager):
    def get_course_by_id(self, course_id):
        return self.get_queryset().filter(id=course_id).first()

    def get_all_active_courses_count(self):
        return self.get_queryset().count()

    def get_course_for_show(self, course_slug):
        return self.get_queryset().filter(slug__iexact=course_slug) \
            .prefetch_related('categories', 'courseprerequisite_set', 'course_levels', 'course_features') \
            .annotate(
            sections_count=Count('coursesection', filter=Q(coursesection__publish_date__lte=datetime.datetime.now())),
            total_section_duration=Sum(F('coursesection__duration__hour') * 60 + F('coursesection__duration__minute'))) \
            .first()

    def filter_courses(self, **kwargs):
        query = self.get_queryset().prefetch_related('main_master', 'main_master__user') \
            .annotate(total_section_duration=Sum(F('coursesection__duration__hour') * 60 + F('coursesection__duration__minute'))) \
            .order_by('-id')
        title = kwargs.get('title')
        categories = kwargs.get('categories')
        course_levels = kwargs.get('course_levels')
        course_states = kwargs.get('course_states')
        course_master_user_id = kwargs.get('master_user_id')

        if title is not None:
            query = query.filter(Q(title__icontains=title) | Q(short_description__icontains=title) | Q(description__icontains=title) | Q(coursetag__title__icontains=title))

        if categories:
            query = query.filter(categories__url_title__in=categories)

        if course_levels is not None and len(course_levels):
            query = query.filter(course_levels__url_title__in=course_levels)

        if course_states is not None and len(course_states):
            query = query.filter(course_status__in=course_states)

        if course_master_user_id is not None:
            query = query.filter(Q(main_master_id=course_master_user_id) | Q(other_masters__user_id=course_master_user_id))

        return query.distinct(), kwargs


def course_introduction_upload_path(instance, filepath):
    name, ext = os.path.splitext(os.path.basename(filepath))
    section_name = get_random_string(75)
    return f"files/introductions/{instance.folder_name}/{section_name}{ext}"


class Course(models.Model):
    class CourseHoldState(models.TextChoices):
        PREPARING = 'PREPARING', _('Preparing')
        ON_PERFORMING = 'ON_PERFORMING', _('On performing')
        FINISHED = 'FINISHED', _('Finished')
        HAS_STOPPED = 'HAS_STOPPED', _('Has stopped')

    title = models.CharField(max_length=300, db_index=True, unique=True, verbose_name=_('Title'))
    slug = models.SlugField(max_length=300, unique=True, verbose_name=_('Course slug field'))
    course_status = models.CharField(max_length=300, choices=CourseHoldState.choices, default=CourseHoldState.PREPARING, verbose_name=_('Course hold status'))
    image = models.ImageField(upload_to='images/course', max_length=200, verbose_name=_('Image'))
    price = models.IntegerField(default=0, verbose_name=_('Price'))
    short_description = models.CharField(max_length=500, verbose_name=_('Short description'))
    description = RichTextField(verbose_name=_('Description'))
    main_master = models.ForeignKey('CourseMaster', related_name='master_courses', on_delete=models.CASCADE, verbose_name=_('Course main master'))
    other_masters = models.ManyToManyField('CourseMaster', blank=True, related_name='other_master_courses', verbose_name=_('Course other masters'))
    course_levels = models.ManyToManyField('CourseLevel', verbose_name=_('Course levels'))
    categories = models.ManyToManyField('CourseCategory', verbose_name=_('Categories'))
    visit_count = models.IntegerField(default=0, verbose_name=_('Visit count'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    can_send_comment = models.BooleanField(default=True, verbose_name=_('Can send comment'))
    show_comments = models.BooleanField(default=True, verbose_name=_('Show comments'))
    estimate_finish_time = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Estimated time to complete the course'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Is deleted'))
    folder_name = models.CharField(max_length=500, unique=True, verbose_name=_('Folder name'))
    video = models.FileField(upload_to=course_introduction_upload_path, null=True, blank=True, max_length=200, verbose_name=_('Video'))

    objects = CourseManager()

    def __str__(self):
        return f'{self.title} / {self.main_master.user}'

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def get_detail_url(self):
        return reverse('courses_detail_page', kwargs={'slug': self.slug})

    def get_course_price_display(self):
        if self.price != 0:
            return '{:,}'.format(self.price) + ' ' + _('Toman')
        else:
            return _('Free')


# endregion

# region course headings

class CourseHeadingManager(models.Manager):
    def get_course_headings_by_course_id(self, course_id):
        return self.get_queryset().order_by('order') \
            .prefetch_related(Prefetch('heading_sections', queryset=CourseSection.objects.filter(publish_date__lte=datetime.datetime.now()))) \
            .filter(course_id=course_id, show_to_user=True)


class CourseHeading(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('Title'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    show_to_user = models.BooleanField(verbose_name=_('Show to user'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name=_('Course'))

    objects = CourseHeadingManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Course heading')
        verbose_name_plural = _('Course headings')


# endregion

# region course sections

def course_section_video_upload_path(instance, filepath):
    name, ext = os.path.splitext(os.path.basename(filepath))
    section_name = get_random_string(75)
    return f"files/courses/{instance.course.folder_name}/videos/{section_name}{ext}"


def course_section_file_upload_path(instance, filepath):
    name, ext = os.path.splitext(os.path.basename(filepath))
    section_name = get_random_string(75)
    return f"files/courses/{instance.course.folder_name}/files/{section_name}{ext}"


class CourseSectionManager(models.Manager):
    pass


class CourseSection(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    duration = models.TimeField(verbose_name=_('Duration'))
    is_free = models.BooleanField(verbose_name=_('Is free'))
    video = models.FileField(upload_to=course_section_video_upload_path, max_length=200, verbose_name=_('Video'))
    file = models.FileField(upload_to=course_section_file_upload_path, max_length=200, verbose_name=_('File'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name=_('Course'))
    course_heading = models.ForeignKey('CourseHeading', related_name='heading_sections', on_delete=models.CASCADE, verbose_name=_('Course heading'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Is deleted'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Publish date'))

    objects = CourseSectionManager()

    def __str__(self):
        return f'{self.title} - {self.duration} - {self.course}'

    class Meta:
        verbose_name = _('Course section')
        verbose_name_plural = _('Course sections')


# endregion

# region course tag

class CourseTag(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name=_('Course'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Course tag')
        verbose_name_plural = _('Course tags')


# endregion

# region course prerequisites


class CoursePrerequisiteManager(models.Manager):
    pass


class CoursePrerequisite(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Title'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Course'))
    course_link = models.ForeignKey('Course', related_name='course_link', verbose_name=_('Course link'), on_delete=models.CASCADE, null=True, blank=True)

    objects = CoursePrerequisiteManager()

    def __str__(self):
        if self.title is not None:
            return f'{self.title}'
        elif self.course is not None:
            return str(self.course)
        else:
            return _('Not set')

    class Meta:
        verbose_name = _('Course prerequisite')
        verbose_name_plural = _('Course prerequisites')


# endregion

# region course visit

class CourseVisitManager(models.Manager):
    def add_visit_for_course(self, user_ip, user_id, course: Course):
        if not self.get_queryset().filter(Q(user_ip=user_ip, course_id=course.id) | Q(user_id=user_id, course_id=course.id)).exists():
            visit = CourseVisit(user_ip=user_ip, course_id=course.id, user_id=user_id or None)
            visit.save()
            course.visit_count += 1
            course.save()


class CourseVisit(models.Model):
    user_ip = models.CharField(max_length=50, verbose_name=_('User ip'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_visits', verbose_name=_('Course'))
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_course_visits', null=True, blank=True, verbose_name=_('User'))

    objects = CourseVisitManager()

    def __str__(self):
        return f'{self.user_ip} / {self.course}'

    class Meta:
        verbose_name = _('Course visit')
        verbose_name_plural = _('Course visits')


# endregion

# region course comment

class CourseCommentManager(models.Manager):
    def get_all_course_active_comments_by_count(self, course_id):
        return self.get_queryset().order_by('-create_date').filter(course_id=course_id, parent__isnull=True, status=CourseComment.CourseCommentStatus.ACCEPTED) \
            .prefetch_related(
            Prefetch('sub_comments', queryset=CourseComment.objects.filter(is_delete=False, status=CourseComment.CourseCommentStatus.ACCEPTED)),
            Prefetch('user')
        )


class CourseComment(models.Model):
    class CourseCommentStatus(models.TextChoices):
        ACCEPTED = 'ACCEPTED', _('Accepted')
        REJECTED = 'REJECTED', _('Rejected')
        UNDER_PROGRESS = 'UNDER_PROGRESS', _('Under progress')

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_courses_comments', verbose_name=_('User'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_comments', verbose_name=_('Course'))
    parent = models.ForeignKey('CourseComment', on_delete=models.CASCADE, related_name='sub_comments', null=True, blank=True, verbose_name=_('Parent comment'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    text = RichTextField(verbose_name=_('Text'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Is deleted'))
    status = models.CharField(max_length=150, choices=CourseCommentStatus.choices, verbose_name=_('Status'))

    objects = CourseCommentManager()

    def __str__(self):
        return f'{self.course} - {self.user}'

    class Meta:
        verbose_name = _('Course comment')
        verbose_name_plural = _('Course comments')


# endregion

# region course features

class CourseFeatures(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('Title'))
    value = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Value'))
    icon = models.CharField(max_length=300, verbose_name=_('Icon'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_features', verbose_name=_('Course'))

    def __str__(self):
        return f'{self.title} / {self.value} / {self.icon}'

    class Meta:
        verbose_name = _('Course feature')
        verbose_name_plural = _('Course features')


# endregion

# region user favorite courses

class UserFavoriteCourseManager(models.Manager):
    pass


class UserFavoriteCourse(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='favorite_courses', verbose_name=_('User'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='user_favorites', verbose_name=_('Course'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))

    objects = UserFavoriteCourseManager()

    def __str__(self):
        return f'{self.user} / {self.course.title}'

    class Meta:
        verbose_name = _('User favorite course')
        verbose_name_plural = _('User favorite courses')

# endregion
