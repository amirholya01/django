# Generated by Django 4.2.7 on 2023-12-13 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_delete_articletag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='categories',
        ),
        migrations.DeleteModel(
            name='ArticleCategory',
        ),
    ]