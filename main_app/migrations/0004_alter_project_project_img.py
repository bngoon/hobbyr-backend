# Generated by Django 5.0.4 on 2024-04-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_project_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_img',
            field=models.ImageField(blank=True, null=True, upload_to='projects/'),
        ),
    ]
