# Generated by Django 2.2.10 on 2020-03-01 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depress', '0002_auto_20200229_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='rule',
            field=models.CharField(default=0, max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='test',
            name='intro',
            field=models.CharField(max_length=1000),
        ),
    ]
