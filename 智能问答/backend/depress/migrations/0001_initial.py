# Generated by Django 2.2.10 on 2020-02-25 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('pid', models.IntegerField()),
                ('answer', models.CharField(max_length=100)),
                ('same_num', models.IntegerField(blank=True)),
                ('score', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('text', models.CharField(max_length=500)),
                ('time', models.DateTimeField()),
                ('send', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField()),
                ('pid', models.IntegerField()),
                ('type', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(max_length=200)),
                ('choice', models.TextField(max_length=500)),
                ('answer', models.TextField(max_length=100)),
                ('explanation', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('time', models.DateTimeField()),
                ('score', models.CharField(max_length=200)),
                ('same_num', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('intro', models.CharField(max_length=300)),
                ('num', models.IntegerField()),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('sex', models.BooleanField(blank=True, null=True)),
                ('address', models.TextField(max_length=50)),
                ('tel', models.CharField(max_length=15)),
            ],
        ),
    ]
