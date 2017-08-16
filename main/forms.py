from django.forms import ModelForm, TextInput
from .models import List, Entry
from django.utils.translation import ugettext as _

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['title']
        widgets = {'title': TextInput(attrs={'class': 'mdc-textfield__input'})}


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'quantity']
        widgets = {'title': TextInput(attrs={'class': 'mdc-textfield__input'}),
                   'quantity': TextInput(attrs={'class': 'mdc-textfield__input',
                                                'type': 'number',
                                                'min': "0"})}
