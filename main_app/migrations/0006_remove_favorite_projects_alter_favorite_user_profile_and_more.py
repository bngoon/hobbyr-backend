# Generated by Django 5.0.4 on 2024-04-10 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_comment_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='projects',
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='main_app.userprofile'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='projects',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='main_app.project'),
            preserve_default=False,
        ),
    ]
