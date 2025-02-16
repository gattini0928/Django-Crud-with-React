# Generated by Django 5.1.6 on 2025-02-15 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_student_user_alter_exam_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='students/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
    ]
