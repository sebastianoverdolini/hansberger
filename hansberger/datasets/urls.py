from django.urls import path
from .views import (
    TextDatasetCreateView,
    TextDatasetDetailView,
)

app_name = 'datasets'
urlpatterns = [
    path('text/create/', view=TextDatasetCreateView.as_view(), name='text-dataset-create'),
    path('text/<slug:dataset_slug>/', view=TextDatasetDetailView.as_view(), name='text-dataset-detail'),
]
