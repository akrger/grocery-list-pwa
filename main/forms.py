from django.forms import ModelForm, TextInput, Select
from .models import List, Entry


class ListForm(ModelForm):

    class Meta:
        model = List
        fields = ['title']
        widgets = {'title': TextInput(attrs={'class': 'mdc-textfield__input'})}


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['grocery_list', 'title', 'quantity', 'category']
        widgets = {
            'grocery_list': Select(attrs={'class': 'mdc-select'}),
            'title': TextInput(attrs={'class': 'mdc-textfield__input'}),
            'category': Select(attrs={'class': 'mdc-select'}),
            'quantity': TextInput(attrs={'class': 'mdc-textfield__input',
                                         'type': 'number',
                                         'min': "1"})}
