from django import forms
from .models import Dataset, FiltrationAnalysis, MapperAnalysis


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


class FiltrationAnalysisCreationForm(forms.ModelForm):
    def __init__(self, research, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research'].initial = research

    class Meta:
        model = FiltrationAnalysis
        exclude = ['slug', 'result_matrix', 'result_plot', 'result_entropy']
        widgets = {'research': forms.HiddenInput}


class MapperAnalysisCreationForm(forms.ModelForm):
    def __init__(self, research, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research'].initial = research

    class Meta:
        model = MapperAnalysis
        exclude = ['slug', 'graph']
        widgets = {'research': forms.HiddenInput}