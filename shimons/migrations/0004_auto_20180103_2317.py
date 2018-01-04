# Generated by Django 2.0 on 2018-01-03 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shimons', '0003_auto_20180103_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jar_path', models.CharField(max_length=255)),
                ('main_jarFile', models.CharField(max_length=128)),
                ('src_path', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patterns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern_path', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RequestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.IntegerField(default=1)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='patterns',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shimons.RequestModel'),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shimons.RequestModel'),
        ),
    ]
