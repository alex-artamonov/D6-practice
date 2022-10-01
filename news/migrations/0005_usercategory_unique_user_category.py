# Generated by Django 4.1.1 on 2022-10-01 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_postcategory_unique_post_category'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='usercategory',
            constraint=models.UniqueConstraint(models.F('user_id'), models.F('category_id'), name='unique_user_category'),
        ),
    ]