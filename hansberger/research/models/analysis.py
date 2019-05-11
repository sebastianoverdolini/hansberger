import ripser
import matplotlib.pyplot as plt
import json
import math
import os.path
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from .research import Research
from .dataset import Dataset


class Analysis(models.Model):
    RELATIVE_STORAGE_PATH = None
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, max_length=110)
    description = models.TextField(max_length=500, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    research = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
        related_name='analysis_set',
        related_query_name='analysis',
    )
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='analysis_set',
        related_query_name='analysis',
    )

    class Meta:
        abstract = True
        unique_together = (('slug', 'research'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.RELATIVE_STORAGE_PATH is None:
            self.RELATIVE_STORAGE_PATH = os.path.join(
                self.research.RELATIVE_STORAGE_PATH,
                'analysis',
                self.slug,
            )


class FiltrationAnalysis(Analysis):
    VIETORIS_RIPS_FILTRATION = 'VRF'
    CLIQUE_WEIGHTED_RANK_FILTRATION = 'CWRF'

    FILTRATION_TYPE_CHOICES = (
        (VIETORIS_RIPS_FILTRATION, 'Vietoris Rips Filtration'),
        (CLIQUE_WEIGHTED_RANK_FILTRATION, 'Clique Weighted Rank Filtration'),
    )

    METRIC_CHOICES = (
        ('braycurtis', 'Braycurtis'),
        ('canberra', 'Canberra'),
        ('chebyshev', 'Chebyshev'),
        ('cityblock', 'City block'),
        ('correlation', 'Correlation'),
        ('cosine', 'Cosine'),
        ('dice', 'Dice'),
        ('euclidean', 'Euclidean'),
        ('hamming', 'Hamming'),
        ('jaccard', 'Jaccard'),
        ('jensenshannon', 'Jensen Shannon'),
        ('kulsinski', 'Kulsinski'),
        ('mahalanobis', 'Mahalonobis'),
        ('matching', 'Matching'),
        ('minkowski', 'Minkowski'),
        ('rogerstanimoto', 'Rogers-Tanimoto'),
        ('russellrao', 'Russel Rao'),
        ('seuclidean', 'Seuclidean'),
        ('sokalmichener', 'Sojal-Michener'),
        ('sokalsneath', 'Sokal-Sneath'),
        ('sqeuclidean', 'Sqeuclidean'),
        ('yule', 'Yule'),
    )

    filtration_type = models.CharField(
        max_length=50,
        choices=FILTRATION_TYPE_CHOICES,
    )
    distance_matrix_metric = models.CharField(
        max_length=20,
        choices=METRIC_CHOICES
    )
    max_homology_dimension = models.IntegerField(default=1)
    max_distances_considered = models.FloatField(default=math.inf)
    coeff = models.IntegerField(default=2)
    do_cocycles = models.BooleanField(default=False)
    n_perm = models.IntegerField(default=None, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('research:filtrationanalysis-detail', (), {
            'filtrationanalysis_slug': self.slug,
            'research_slug': self.research.slug,
        })

    def execute(self):
        rips = ripser.Rips(
            maxdim=self.max_homology_dimension,
            thresh=self.max_distances_considered,
            coeff=self.coeff,
            do_cocycles=self.do_cocycles,
            n_perm=self.n_perm,
        )

        if self.filtration_type is self.VIETORIS_RIPS_FILTRATION:
            matrix_to_analyze = self.dataset.get_distance_matrix(self.distance_matrix_metric)
        elif self.filtration_type is self.CLIQUE_WEIGHTED_RANK_FILTRATION:
            matrix_to_analyze = self.dataset.get_correlation_matrix()
        else:
            raise ValueError("Invalid filtration type.")

        analysis_result_matrix = rips.fit_transform(matrix_to_analyze, distance_matrix=True)
        self.__save_plot(rips)
        self.__save_matrix_json([l.tolist() for l in analysis_result_matrix])

    def __save_plot(self, rips):
        plot_filename = self.slug + '_plot.svg'
        absolute_storage_path = os.path.join(settings.MEDIA_ROOT, self.RELATIVE_STORAGE_PATH)
        if not os.path.exists(absolute_storage_path):
            os.makedirs(absolute_storage_path)
        rips.plot()
        plt.savefig(os.path.join(absolute_storage_path, plot_filename))
        self.result_plot = os.path.join(self.RELATIVE_STORAGE_PATH, plot_filename)

    def __save_matrix_json(self, matrix):
        self.result_matrix = json.dumps(matrix)
