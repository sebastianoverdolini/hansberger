from django import forms
from .models import Dataset


class DatasetCreationForm(forms.ModelForm):
    def __init__(self, research, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research'].initial = research

    class Meta:
        model = Dataset
        fields = ['name', 'file_type', 'description', 'file', 'research']
        widgets = {'research': forms.HiddenInput}


class TextDatasetProcessForm(forms.Form):

    values_separator_character = forms.CharField(
        max_length=5,
        label="separator character of the values in the file"
    )
    identity_column_index = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
        label="column number that identifies the progressive number of rows in the file"
    )
    header_row_index = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
        label="row number that identifies the column in the file"
    )
