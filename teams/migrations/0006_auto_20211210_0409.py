# Generated by Django 3.1.7 on 2021-12-10 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_team_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='tid',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
