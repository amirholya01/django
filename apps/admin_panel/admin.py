from django.contrib import admin
from . import models as domains


# region account

@admin.register(domains.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    list_editable = ['first_name', 'last_name', 'is_active']
    list_filter = ['is_active']


# endregion

# region settings

@admin.register(domains.SiteSetting)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'domain_name', 'tell', 'mobile', 'support_email']
    list_editable = ['domain_name', 'tell', 'support_email']


@admin.register(domains.DynamicLink)
class DynamicLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'position', 'is_active']
    list_editable = ['url', 'order', 'position', 'is_active']
    list_filter = ['position']
    autocomplete_fields = ['parent']
    search_fields = ['title']


@admin.register(domains.DynamicPage)
class DynamicPagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'get_url', 'is_active']
    list_editable = ['url_title', 'is_active']


# endregion

# region ticket

@admin.register(domains.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'ticket_state')
    list_filter = ('ticket_state', 'ticket_priority', 'ticket_section')


@admin.register(domains.TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    pass


# endregion

# region articles

@admin.register(domains.Article)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title', 'author', 'create_date', 'publish_date')
    list_editable = ['title']
    autocomplete_fields = ['author']
    search_fields = ['title', 'author']


@admin.register(domains.ArticleComment)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('article', 'sender', 'comment_state', 'create_date')
    list_editable = ('comment_state',)


# endregion

# region contact us

@admin.register(domains.ContactUs)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'full_name', 'create_date', 'is_seen')
    list_editable = ('full_name', 'is_seen')
    list_filter = ('is_seen',)


# endregion

# region courses

@admin.register(domains.CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active']
    list_editable = ['url_title', 'is_active']
    autocomplete_fields = ['parent']
    search_fields = ['title', 'url_title']


@admin.register(domains.CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'order']
    list_editable = ['url_title', 'order']


@admin.register(domains.CourseTag)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(domains.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'main_master', 'folder_name', 'can_send_comment', 'course_status']
    list_editable = ['price', 'can_send_comment', 'course_status', 'folder_name']
    autocomplete_fields = ['other_masters']
    search_fields = ['title', 'price']
    list_filter = ['course_status']


@admin.register(domains.CourseHeading)
class CourseHeadingAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course']
    search_fields = ['title']
    list_display = ['title', 'order', 'show_to_user', 'course']
    list_editable = ['order', 'show_to_user']


@admin.register(domains.CoursePrerequisite)
class CoursePrerequisiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']
    list_editable = ['order']
    autocomplete_fields = ['course', 'course_link']
    search_fields = ['title']


@admin.register(domains.CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'duration']
    list_editable = ['order', 'duration']
    autocomplete_fields = ['course', 'course_heading']


@admin.register(domains.CourseVisit)
class CourseVisitAdmin(admin.ModelAdmin):
    list_display = ['user_ip', 'create_date', 'course']


@admin.register(domains.CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'create_date', 'status']
    list_editable = ['status']
    autocomplete_fields = ['user', 'course', 'parent']
    search_fields = ['user', 'course', 'text']
    list_filter = ['status']


@admin.register(domains.CourseFeatures)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'value', 'icon']
    list_editable = ['title', 'value', 'icon']
    autocomplete_fields = ['course']


@admin.register(domains.UserFavoriteCourse)
class UserFavoriteCourseAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'course']
    autocomplete_fields = ['user', 'course']


# endregion

# region masters

@admin.register(domains.CourseMaster)
class CourseMasterAdmin(admin.ModelAdmin):
    list_display = ['show_master_name', 'show_in_list', 'default_share_percentage']
    list_editable = ['show_in_list', 'default_share_percentage']
    search_fields = ['user']
    autocomplete_fields = ['user']


# endregion

# region wallet

@admin.register(domains.UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'transaction_type', 'transaction_way', 'transaction_for', 'is_paid', 'tracking_code', 'payment_date']
    list_editable = ['price', 'price', 'transaction_type', 'transaction_way', 'transaction_for', 'is_paid']
    autocomplete_fields = ['user']
    list_filter = ['is_paid', 'transaction_way', 'transaction_for', 'transaction_type']
    search_fields = ['price', 'tracking_code']

# endregion
