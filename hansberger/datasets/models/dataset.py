from enum import Enum
import scipy.spatial.distance as distance
import numpy
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
from django.urls import reverse_lazy
from research.models import Research


class DatasetKindChoice(Enum):
    TEXT = "Text"
    EDF = "EDF"


class Dataset(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(db_index=True, max_length=150)
    description = models.TextField(max_length=500, blank=True, null=True)
    kind = models.CharField(
        max_length=10,
        choices=[(kind.name, kind.value) for kind in DatasetKindChoice]
    )
    source = models.FileField()
    creation_date = models.DateField(auto_now_add=True)
    research = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
        related_name='datasets',
        related_query_name='dataset'
    )
    data = JSONField(blank=True, null=True)
    rows = models.PositiveIntegerField(blank=True, null=True)
    cols = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-creation_date']
        unique_together = (('slug', 'research'))
        verbose_name = "dataset"
        verbose_name_plural = "datasets"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy(
            'datasets:dataset-detail',
            kwargs={
                'research_slug': self.research.slug,
                'dataset_slug': self.slug,
            }
        )

    def get_distance_matrix(self, metric):
        return distance_matrix(self.data, metric)

    def get_correlation_matrix(self):
        return correlation_matrix(self.data)

    def split_matrix(self, window, overlap):  # returns a generator
        # matrix = numpy.array(self.data).transpose()
        matrix = self.data
        cols = len(matrix[0])
        step = window - overlap
        windows = 1 + (cols - window) // step

        for i in range(windows):
            tmp = matrix[:, window*i - overlap*i: window*(i+1) - overlap*i]
            yield tmp


def distance_matrix(matrix, metric):
    return distance.squareform(distance.pdist(
                numpy.array(matrix).transpose(),
                metric=metric
            ))


def correlation_matrix(matrix):
    return numpy.corrcoef(numpy.array(matrix))
