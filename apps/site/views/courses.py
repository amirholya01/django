import datetime
from django.contrib import messages
from django.core.paginator import Paginator, Page
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from apps.site.forms.courses_form import AddCourseCommentForm
from utilities.web.http import get_client_ip
from apps.admin_panel import models as domains


# region courses list


class CoursesListView(View):
    def get(self, request: HttpRequest):
        query, filter_data = domains.Course.objects.filter_courses(
            title=request.GET.get('title'),
            categories=request.GET.getlist(key='categories'),
            course_levels=request.GET.getlist(key='course_levels'),
            course_states=[domains.Course.CourseHoldState.ON_PERFORMING, domains.Course.CourseHoldState.FINISHED]
        )
        paginator = Paginator(query, 6)
        page_obj: Page = paginator.get_page(request.GET.get('page'))

        context = {
            'paginator': paginator,
            'page_obj': page_obj,
            'categories': domains.CourseCategory.objects.get_all_active_categories_with_sub_categories(),
            'filter_items': filter_data,
            'course_levels': domains.CourseLevel.objects.get_all_levels_by_order(),
        }

        return render(request, 'site/courses/course_list.html', context)


# endregion

# region course detail

class CourseDetailView(View):
    def get(self, request, slug):
        course: domains.Course = domains.Course.objects.get_course_for_show(slug)

        if course is None:
            raise Http404(_('Information not found'))

        domains.CourseVisit.objects.add_visit_for_course(get_client_ip(request), request.user.id or None, course)
        comment_form = AddCourseCommentForm(initial={'course_id': course.id})
        context = {
            'course': course,
            'main_category': course.categories.all().filter(parent_id__isnull=True).first(),
            'course_headings': domains.CourseHeading.objects.get_course_headings_by_course_id(course.id),
            'course_main_master': domains.CourseMaster.objects.get_by_master_id(course.main_master_id),
            'comments': not course.show_comments or domains.CourseComment.objects.get_all_course_active_comments_by_count(course.id),
            'form': comment_form
        }
        return render(request, 'site/courses/course_detail.html', context)


# endregion

# region submit course comment

class SubmitCourseCommentView(View):
    def post(self, request: HttpRequest):
        comment_form = AddCourseCommentForm(request.POST or None)
        if comment_form.is_valid():
            course = domains.Course.objects.get_course_by_id(comment_form.cleaned_data.get('course_id'))
            if course is not None:
                if course.can_send_comment:
                    if request.user.is_authenticated:
                        new_comment = domains.CourseComment(
                            user_id=request.user.id,
                            course_id=course.id,
                            text=comment_form.cleaned_data.get('text'),
                            parent_id=comment_form.cleaned_data.get('comment_id'),
                            is_delete=False,
                            status=domains.CourseComment.CourseCommentStatus.UNDER_PROGRESS,
                            create_date=datetime.datetime.now()
                        )
                        new_comment.save()
                        messages.add_message(request, messages.SUCCESS, _('Your comment has been sent successfully and will be shown after studying'))
                    else:
                        messages.add_message(request, messages.WARNING, _('You should login first'))
                else:
                    messages.add_message(request, messages.ERROR, _('Can not send comment for this course'))
            else:
                raise Http404(_('Not found'))
        else:
            messages.add_message(request, messages.ERROR, _('Please enter your comment'))
        course = domains.Course.objects.get_course_by_id(comment_form.cleaned_data.get('course_id'))
        return redirect(course.get_detail_url())

# endregion
