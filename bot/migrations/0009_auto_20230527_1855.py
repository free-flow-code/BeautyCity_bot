# Generated by Django 2.2.24 on 2023-05-27 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
    ]
