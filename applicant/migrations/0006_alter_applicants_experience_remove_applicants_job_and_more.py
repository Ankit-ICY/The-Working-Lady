# Generated by Django 4.2.9 on 2024-03-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0005_work_category_remove_applicants_job_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicants',
            name='experience',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='applicants',
            name='job',
        ),
        migrations.AlterField(
            model_name='applicants',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='applicants',
            name='job',
            field=models.ManyToManyField(to='applicant.work'),
        ),
    ]
