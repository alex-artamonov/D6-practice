# Generated by Django 4.1.1 on 2022-10-01 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_usercategory_category_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='postcategory',
            constraint=models.UniqueConstraint(models.F('post_id'), models.F('category_id'), name='unique_post_category'),
        ),
    ]