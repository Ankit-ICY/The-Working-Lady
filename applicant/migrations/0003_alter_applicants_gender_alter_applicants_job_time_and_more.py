# Generated by Django 5.0.3 on 2024-03-23 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0002_alter_applicants_job_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicants',
            name='gender',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='applicants',
            name='job_time',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='applicants',
            name='language',
            field=models.CharField(max_length=10),
        ),
    ]
