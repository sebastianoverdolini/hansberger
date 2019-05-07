# Generated by Django 2.0.13 on 2019-05-07 18:04

from django.db import migrations, models
import django.db.models.deletion
import research.models.dataset.dataset


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='file',
            field=models.FileField(upload_to=research.models.dataset.dataset.dataset_directory_path),
        ),
        migrations.AlterField(
            model_name='filtrationanalysis',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis_set', related_query_name='analysis', to='research.Dataset'),
        ),
        migrations.AlterField(
            model_name='filtrationanalysis',
            name='result_plot',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]