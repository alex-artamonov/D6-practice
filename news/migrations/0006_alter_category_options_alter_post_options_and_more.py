# Generated by Django 4.1.1 on 2022-10-03 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_usercategory_unique_user_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-name']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_dtm']},
        ),
        migrations.AlterField(
            model_name='author',
            name='rating',
            field=models.SmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_dtm',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.SmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('NWS', 'новость'), ('ACL', 'статья')], max_length=3, verbose_name='Тип'),
        ),
    ]
