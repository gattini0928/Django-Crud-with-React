# Generated by Django 5.1.6 on 2025-02-20 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_student_student_status_delete_schoolsubject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teachers',
        ),
        migrations.AddField(
            model_name='student',
            name='teachers',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to='api.teacher'),
        ),
    ]
