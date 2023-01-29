# Generated by Django 3.1.7 on 2021-11-28 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.IntegerField(null=True)),
                ('pid', models.BigIntegerField(null=True)),
                ('gid', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('archived', models.BooleanField(default=False)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
            options={
                'ordering': ['oid'],
            },
        ),
    ]
