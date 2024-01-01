from django.urls import path
from .views import home, account, articles, courses

urlpatterns = [
    # home
    path('', home.home_page, name='home_page'),
    path('contact-us/', home.ContactView.as_view(), name='contact_us_page'),
    path('about-us/', home.about_us_view, name='about_us_page'),
    path('page/<str:url_title>', home.dynamic_page, name='dynamic_page_view'),
    # account
    path('register/', account.RegisterPage.as_view(), name='register_page'),
    path('login/', account.LoginPage.as_view(), name='login_page'),
    path('logout/', account.LogoutPage.as_view(), name='logout_page'),
    path('forgot-pass/', account.ForgotPasswordPage.as_view(), name='forgot_password_page'),
    path('reset-pass/<str:email_active_code>', account.ResetPasswordPage.as_view(), name='reset_password_page'),
    path('activate-account/<email_active_code>', account.ActivateAccountPage.as_view(), name='activate_account_page'),
    # articles
    path('a/<int:article_id>', articles.article_short_link, name='articles_short_link_page'),
    path('articles/', articles.ArticlesPage.as_view(), name='articles_list_page'),
    path('articles/add-comment/<int:article_id>', articles.AddArticleCommentPage.as_view(), name='add_article_comment_page'),
    path('articles/<int:article_id>/<str:article_title>', articles.ArticleDetailPage.as_view(), name='articles_detail_page'),
    # courses
    path('courses/', courses.CoursesListView.as_view(), name='courses_list_page'),
    path('courses/add-course-comment', courses.SubmitCourseCommentView.as_view(), name='add_course_comment'),
    path('courses/<slug:slug>', courses.CourseDetailView.as_view(), name='courses_detail_page'),
]
