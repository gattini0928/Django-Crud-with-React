# Generated by Django 5.1.6 on 2025-02-19 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_student_photo_alter_teacher_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_status',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='SchoolSubject',
        ),
    ]
