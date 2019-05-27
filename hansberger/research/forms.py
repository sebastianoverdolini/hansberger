from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from django.urls import reverse_lazy
from .models import Dataset, FiltrationAnalysis, MapperAnalysis
import numpy


class DatasetCreationForm(forms.ModelForm):
    def __init__(self, research, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research'].initial = research

    class Meta:
        model = Dataset
        fields = ['name', 'source_type', 'description', 'source', 'research']
        widgets = {'research': forms.HiddenInput}


class TextDatasetProcessForm(forms.Form):

    values_separator_character = forms.CharField(
        max_length=5,
        label="separator character of the values in the file",
        initial=','
    )
    identity_column_index = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
        label="column number that identifies the progressive number of rows in the file",
        initial=0
    )
    header_row_index = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
        label="row number that identifies the column in the file",
        initial=0
    )


def raise_window_warning(dataset, window_size, window_overlap):
    matrix = numpy.array(dataset.data).transpose()
    cols = len(matrix[0])
    step = window_size - window_overlap
    return bool((cols-window_size) % step)


def window_overlap_checks(window_size, window_overlap, dataset):
    if window_size <= 0:
        raise forms.ValidationError("Window size can't be less than or equal to 0")
    if dataset and window_size > len(dataset.data[0]):
        raise forms.ValidationError("Window size can't be greater than the number of columns in the dataset")
    if window_overlap < 0:
        raise forms.ValidationError("Window overlap can't be less than 0")
    if window_overlap >= window_size:
        raise forms.ValidationError("Window overlap can't be greater than or equal to window size")
    if raise_window_warning(dataset, window_size, window_overlap):
        pass


class FiltrationAnalysisCreationForm(forms.ModelForm):
    def __init__(self, research, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research'].initial = research
        '''
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse_lazy('research:filtrationanalysis-create', kwargs={
                                 'research_slug': research.slug})
        self.helper.layout = Layout(
            'name',
            'description',
            'dataset',
            'precomputed_distance_matrix',
            'window_size',
            'window_overlap',
            'filtration_type',
            'distance_matrix_metric',
            Fieldset(
                'first arg is the legend of the fieldset',
                'max_homology_dimension',
                'max_distances_considered',
                'coeff',
                'do_cocycles',
                'n_perm'
            )
        )
        '''

    def clean(self):
        cleaned_data = super(FiltrationAnalysisCreationForm, self).clean()
        dataset = cleaned_data.get("dataset")
        precomputed_distance_matrix = cleaned_data.get("precomputed_distance_matrix")
        filtration_type = cleaned_data.get("filtration_type")
        distance_matrix_metric = cleaned_data.get("distance_matrix_metric")
        window_overlap = cleaned_data.get("window_overlap")
        window_size = cleaned_data.get("window_size")
        filtration_type = cleaned_data.get("filtration_type")
        if window_size is not None:
            window_overlap_checks(window_size, window_overlap, dataset)

        if dataset and precomputed_distance_matrix:  # both fields were filled
            raise forms.ValidationError("""You must either provide a precomputed distance matrix or select a dataset,
                                         not both.""")
        elif not (dataset or precomputed_distance_matrix):  # neither one was filled
            raise forms.ValidationError("You must either provide a precomputed distance matrix or select a dataset")

        if (filtration_type == FiltrationAnalysis.VIETORIS_RIPS_FILTRATION and distance_matrix_metric == '' and
           not precomputed_distance_matrix):
            raise forms.ValidationError("You must provide a distance matrix metric for a Vietoris-Rips Filtration")

    class Meta:
        model = FiltrationAnalysis
        exclude = ['slug', 'result_matrix', 'result_plot', 'result_entropy']
        widgets = {'research': forms.HiddenInput}


class MapperAnalysisCreationForm(forms.ModelForm):
    def __init__(self, research, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research'].initial = research

    def clean(self):
        cleaned_data = super(MapperAnalysisCreationForm, self).clean()
        dataset = cleaned_data.get("dataset")
        precomputed_distance_matrix = cleaned_data.get("precomputed_distance_matrix")
        window_overlap = cleaned_data.get("window_overlap")
        window_size = cleaned_data.get("window_size")
        if window_size is not None:
            window_overlap_checks(window_size, window_overlap, dataset)
        if dataset and precomputed_distance_matrix:  # both fields were filled
            raise forms.ValidationError("""You must either provide a precomputed distance matrix or select a dataset,
                                         not both.""")
        elif not (dataset or precomputed_distance_matrix):  # neither one was filled
            raise forms.ValidationError("You must either provide a precomputed distance matrix or select a dataset")

    class Meta:
        model = MapperAnalysis
        exclude = ['slug', 'graph']
        widgets = {'research': forms.HiddenInput}
