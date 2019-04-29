from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
import math
from .research import Research


class Analysis(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, max_length=110)
    description = models.TextField(max_length=500, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    research = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
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


class FiltrationAnalysis(Analysis):
    VIETORIS_RIPS_FILTRATION = 'VietorisRipsFiltration'
    CLIQUE_WEIGHTED_RANK_FILTRATION = 'CliqueWeightedRankFiltration'

    FILTRATION_TYPE_CHOICES = (
        (VIETORIS_RIPS_FILTRATION, 'Vietoris Rips Filtration'),
        (CLIQUE_WEIGHTED_RANK_FILTRATION, 'Clique Weighted Rank Filtration'),
    )

    METRIC_CHOICES = (
        ('braycurtis', 'Braycurtis'), ('canberra', 'Canberra'), ('chebyshev', 'Chebyshev'), ('cityblock', 'City block'),
        ('correlation', 'Correlation'), ('cosine', 'Cosine'), ('dice', 'Dice'), ('euclidean', 'Euclidean'),
        ('hamming', 'Hamming'), ('jaccard', 'Jaccard'), ('jensenshannon', 'Jensen Shannon'), ('kulsinski', 'Kulsinski'),
        ('mahalanobis', 'Mahalonobis'), ('matching', 'Matching'), ('minkowski', 'Minkowski'),
        ('rogerstanimoto', 'Rogers-Tanimoto'), ('russellrao', 'Russel Rao'), ('seuclidean', 'Seuclidean'),
        ('sokalmichener', 'Sojal-Michener'), ('sokalsneath', 'Sokal-Sneath'), ('sqeuclidean', 'Sqeuclidean'),
        ('yule', 'Yule')
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
    n_perm = models.IntegerField(default=None, null=True)

    analysis_result_matrix = JSONField(blank=True, null=True)
    plot = models.ImageField(blank=True, null=True)
