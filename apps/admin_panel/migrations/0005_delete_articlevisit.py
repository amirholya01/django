# Generated by Django 4.2.7 on 2023-12-13 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_remove_article_categories_delete_articlecategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleVisit',
        ),
    ]