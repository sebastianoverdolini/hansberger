# Generated by Django 2.0.13 on 2019-04-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0003_auto_20190424_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='plot',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]