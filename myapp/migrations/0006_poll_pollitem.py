# Generated by Django 2.1.2 on 2018-11-01 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_diary_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('enable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PollItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image_url', models.CharField(blank=True, max_length=200, null=True)),
                ('vote', models.PositiveIntegerField(default=0)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Poll')),
            ],
        ),
    ]