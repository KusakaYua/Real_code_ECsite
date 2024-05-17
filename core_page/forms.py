from django import forms
from .models import Category


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})

    category = forms.ModelChoiceField(queryset=Category.objects, label='カテゴリ', empty_label='選択してください')
