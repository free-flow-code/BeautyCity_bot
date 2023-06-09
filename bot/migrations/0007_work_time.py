# Generated by Django 2.2.24 on 2023-05-27 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20230525_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work_time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='DD-MM-YYYY', verbose_name='Дата работы')),
                ('timeslot_start', models.IntegerField(choices=[(0, '09:00 – 09:30'), (1, '09:30 – 10:00'), (2, '10:00 – 10:30'), (3, '10:30 – 11:00'), (4, '11:00 – 11:30'), (5, '11:30 – 12:00'), (6, '12:00 – 12:30'), (7, '12:30 – 13:00'), (8, '13:00 – 13:30'), (9, '13:30 – 14:00'), (10, '14:00 – 14:30'), (11, '14:30 – 15:00'), (12, '15:00 – 15:30'), (13, '16:00 – 16:30'), (14, '17:00 – 17:30'), (15, '17:30 – 18:00'), (16, '18:00 – 18:30'), (17, '18:30 – 19:00'), (18, '19:00 – 19:30'), (19, '19:30 – 20:00')], null=True, verbose_name='Время начала работы')),
                ('timeslot_end', models.IntegerField(choices=[(0, '09:00 – 09:30'), (1, '09:30 – 10:00'), (2, '10:00 – 10:30'), (3, '10:30 – 11:00'), (4, '11:00 – 11:30'), (5, '11:30 – 12:00'), (6, '12:00 – 12:30'), (7, '12:30 – 13:00'), (8, '13:00 – 13:30'), (9, '13:30 – 14:00'), (10, '14:00 – 14:30'), (11, '14:30 – 15:00'), (12, '15:00 – 15:30'), (13, '16:00 – 16:30'), (14, '17:00 – 17:30'), (15, '17:30 – 18:00'), (16, '18:00 – 18:30'), (17, '18:30 – 19:00'), (18, '19:00 – 19:30'), (19, '19:30 – 20:00')], null=True, verbose_name='Время окончания работы')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='specialist', to='bot.Specialist', verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Время работы специалиста',
                'verbose_name_plural': 'Время работы специалистов',
            },
        ),
    ]
