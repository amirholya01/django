# Generated by Django 4.2.7 on 2023-12-11 19:14

import apps.admin_panel.models.courses_models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='Article slug field')),
                ('short_description', models.CharField(max_length=200, verbose_name='Short description')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Text')),
                ('image', models.ImageField(max_length=300, upload_to='images/article', verbose_name='Image')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('publish_date', models.DateTimeField(verbose_name='Publish date')),
                ('visit_count', models.IntegerField(default=0, verbose_name='Visit count')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('can_add_comment', models.BooleanField(default=True, verbose_name='Can add comment')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('url_title', models.CharField(max_length=200, unique=True, verbose_name='Url title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, max_length=200, null=True, upload_to='images/article-category', verbose_name='Image')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
            ],
            options={
                'verbose_name': 'Article category',
                'verbose_name_plural': 'Article categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='Course slug field')),
                ('course_status', models.CharField(choices=[('PREPARING', 'Preparing'), ('ON_PERFORMING', 'On performing'), ('FINISHED', 'Finished'), ('HAS_STOPPED', 'Has stopped')], default='PREPARING', max_length=300, verbose_name='Course hold status')),
                ('image', models.ImageField(max_length=200, upload_to='images/course', verbose_name='Image')),
                ('price', models.IntegerField(default=0, verbose_name='Price')),
                ('short_description', models.CharField(max_length=500, verbose_name='Short description')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('visit_count', models.IntegerField(default=0, verbose_name='Visit count')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('can_send_comment', models.BooleanField(default=True, verbose_name='Can send comment')),
                ('show_comments', models.BooleanField(default=True, verbose_name='Show comments')),
                ('estimate_finish_time', models.CharField(blank=True, max_length=300, null=True, verbose_name='Estimated time to complete the course')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('folder_name', models.CharField(max_length=500, unique=True, verbose_name='Folder name')),
                ('video', models.FileField(blank=True, max_length=200, null=True, upload_to=apps.admin_panel.models.courses_models.course_introduction_upload_path, verbose_name='Video')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseHeading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('show_to_user', models.BooleanField(verbose_name='Show to user')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Course heading',
                'verbose_name_plural': 'Course headings',
            },
        ),
        migrations.CreateModel(
            name='CourseLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('url_title', models.CharField(max_length=200, verbose_name='Url title')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Course level',
                'verbose_name_plural': 'Course levels',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('ticket_section', models.CharField(choices=[('SUPPORT', 'Support'), ('Technical', 'Technical'), ('Financial', 'Financial')], default='Technical', max_length=300, verbose_name='Ticket section')),
                ('ticket_state', models.CharField(choices=[('Answered', 'Answered'), ('NotAnswered', 'Not answered'), ('Closed', 'Closed'), ('UnderProgress', 'Under progress')], default='NotAnswered', max_length=300, verbose_name='Ticket state')),
                ('ticket_priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=300, verbose_name='Priority')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('is_delete', models.BooleanField(verbose_name='Deleted or not')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, verbose_name='Price')),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal')], max_length=200, verbose_name='Transaction type')),
                ('transaction_way', models.CharField(choices=[('ONLINE', 'Online'), ('CASH', 'CASH'), ('CHARGE_BY_ADMIN', 'Charge by admin'), ('CARD_TO_CARD', 'Card to card')], max_length=200, verbose_name='Transaction way')),
                ('transaction_for', models.CharField(choices=[('DISCOUNT', 'Discount'), ('BUY_COURSE', 'Buy course'), ('CHARGE', 'Charge wallet'), ('CHECK_OUT', 'Checkout'), ('REQUEST_CERTIFICATE', 'Request certificate'), ('REFUND', 'Refund'), ('CONSULT', 'Consult'), ('OTHER', 'Other')], max_length=200, verbose_name='Transaction for')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is paid')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='Payment date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('user_ip', models.CharField(blank=True, max_length=50, null=True, verbose_name='User IP')),
                ('authority', models.CharField(blank=True, max_length=50, null=True, verbose_name='Authority')),
                ('tracking_code', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tracking code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User wallet',
                'verbose_name_plural': 'User wallets',
            },
        ),
        migrations.CreateModel(
            name='UserFavoriteCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to='admin_panel.course', verbose_name='Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_courses', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User favorite course',
                'verbose_name_plural': 'User favorite courses',
            },
        ),
        migrations.CreateModel(
            name='TicketMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Text')),
                ('is_delete', models.BooleanField(verbose_name='Deleted or not')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.ticket', verbose_name='Ticket')),
            ],
            options={
                'verbose_name': 'Ticket message',
                'verbose_name_plural': 'Ticket messages',
            },
        ),
        migrations.CreateModel(
            name='CourseVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.CharField(max_length=50, verbose_name='User ip')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_visits', to='admin_panel.course', verbose_name='Course')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_course_visits', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Course visit',
                'verbose_name_plural': 'Course visits',
            },
        ),
        migrations.CreateModel(
            name='CourseTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Course tag',
                'verbose_name_plural': 'Course tags',
            },
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('duration', models.TimeField(verbose_name='Duration')),
                ('is_free', models.BooleanField(verbose_name='Is free')),
                ('video', models.FileField(max_length=200, upload_to=apps.admin_panel.models.courses_models.course_section_video_upload_path, verbose_name='Video')),
                ('file', models.FileField(max_length=200, upload_to=apps.admin_panel.models.courses_models.course_section_file_upload_path, verbose_name='File')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('publish_date', models.DateTimeField(blank=True, null=True, verbose_name='Publish date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.course', verbose_name='Course')),
                ('course_heading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heading_sections', to='admin_panel.courseheading', verbose_name='Course heading')),
            ],
            options={
                'verbose_name': 'Course section',
                'verbose_name_plural': 'Course sections',
            },
        ),
        migrations.CreateModel(
            name='CoursePrerequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Title')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.course', verbose_name='Course')),
                ('course_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_link', to='admin_panel.course', verbose_name='Course link')),
            ],
            options={
                'verbose_name': 'Course prerequisite',
                'verbose_name_plural': 'Course prerequisites',
            },
        ),
        migrations.CreateModel(
            name='CourseMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_in_list', models.BooleanField(default=True, verbose_name='Show in list')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('default_share_percentage', models.IntegerField(default=0, verbose_name='Default share percentage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Course master',
                'verbose_name_plural': 'Course masters',
            },
        ),
        migrations.CreateModel(
            name='CourseFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('value', models.CharField(blank=True, max_length=300, null=True, verbose_name='Value')),
                ('icon', models.CharField(max_length=300, verbose_name='Icon')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_features', to='admin_panel.course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Course feature',
                'verbose_name_plural': 'Course features',
            },
        ),
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Text')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('status', models.CharField(choices=[('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('UNDER_PROGRESS', 'Under progress')], max_length=150, verbose_name='Status')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_comments', to='admin_panel.course', verbose_name='Course')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_comments', to='admin_panel.coursecomment', verbose_name='Parent comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_courses_comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Course comment',
                'verbose_name_plural': 'Course comments',
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Title')),
                ('url_title', models.CharField(max_length=200, unique=True, verbose_name='Url title')),
                ('icon_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Icon name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/course-category', verbose_name='Image')),
                ('short_description', models.CharField(max_length=1000, verbose_name='Short description')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.coursecategory', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Course category',
                'verbose_name_plural': 'Course categories',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(to='admin_panel.coursecategory', verbose_name='Categories'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_levels',
            field=models.ManyToManyField(to='admin_panel.courselevel', verbose_name='Course levels'),
        ),
        migrations.AddField(
            model_name='course',
            name='main_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master_courses', to='admin_panel.coursemaster', verbose_name='Course main master'),
        ),
        migrations.AddField(
            model_name='course',
            name='other_masters',
            field=models.ManyToManyField(blank=True, related_name='other_master_courses', to='admin_panel.coursemaster', verbose_name='Course other masters'),
        ),
        migrations.CreateModel(
            name='ArticleVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.CharField(max_length=20, verbose_name='User ip')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.article', verbose_name='Article')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Article visit',
                'verbose_name_plural': 'Article visits',
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.article', verbose_name='Article')),
            ],
            options={
                'verbose_name': 'Article tag',
                'verbose_name_plural': 'Article tags',
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Text')),
                ('comment_state', models.CharField(choices=[('NotSeen', 'Not seen'), ('Accepted', 'Accepted'), ('NotAccepted', 'Not accepted')], default='NotSeen', max_length=200, verbose_name='Comment state')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.article', verbose_name='Article')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.articlecomment', verbose_name='Parent comment')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name': 'Article comment',
                'verbose_name_plural': 'Article comments',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='admin_panel.articlecategory', verbose_name='Categories'),
        ),
        migrations.AddField(
            model_name='article',
            name='related_articles',
            field=models.ManyToManyField(blank=True, to='admin_panel.article', verbose_name='Related articles'),
        ),
    ]
