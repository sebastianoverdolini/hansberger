# Generated by Django 2.0.13 on 2019-06-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0003_auto_20190604_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtrationanalysis',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='filtrationwindow',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mapperanalysis',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mapperwindow',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
