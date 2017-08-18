from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import List, Entry
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from .forms import ListForm, EntryForm


@login_required
def index(request):
    toolbarTitle = _("All Grocery Lists")
    user = request.user.id
    lists = List.objects.all().filter(user=user)
    return render(request, "main/index.html",
                  {"toolbarTitle": toolbarTitle,
                   "lists": lists})


class ShowListView(TemplateView):
    template_name = "main/show_list.html"
    form_class = ListForm

    def get(self, request, list_id):
        _list = get_object_or_404(List, id=list_id)
        form = ListForm(request.POST or None, instance=_list)
        entries = Entry.objects.all().filter(grocery_list=list_id)
        print(_list.get_entry_order())


# _dict = OrderedDict( {7 :'DR', 2:'FO', 1:'DR', 8: 'DR', 10: 'ZU'} )
# _list = ['FO', 'DR' , 'ZU']
# index_map = {v: i for i, v in enumerate(_list)}
# #index_map = OrderedDict((v, i) for i, v in enumerate(_list))
# print(OrderedDict(sorted(_dict.items(), key=lambda pair: index_map[pair[1]])))

        return render(request, self.template_name,
                      {"toolbarTitle": _list.title,
                       "entries": entries,
                       'list_id': list_id,
                       'form': form})


@login_required
def show_all_entries(request):
    entries = dict()
    toolbarTitle = _("All Entries")
    # very hacky, but neccessary with sqlite
    for p in Entry.objects.values_list('id', 'title', 'category').distinct():
        choice = {k: v for k, v in Entry.CATEGORIES}[p[-1]]
        entries[p[1]] = [p[0], choice]
    return render(request, "main/show_all_entries.html",
                  {"entries": entries,
                   'toolbarTitle': toolbarTitle})


class EditEntryView(TemplateView):
    template_name = "main/edit_entry.html"
    toolbarTitle = _("Edit Entry")

    def get(self, request, entry_id):
        entry = get_object_or_404(Entry, id=entry_id)
        form = EntryForm(instance=entry)
        return render(request, self.template_name,
                      {"form": form,
                       'toolbarTitle': self.toolbarTitle})

    def post(self, request, entry_id, *args, **kwargs):
        form = EntryForm(data=request.POST)
        entry = get_object_or_404(Entry, id=entry_id)
        if form.is_valid():
            entry.grocery_list = form.cleaned_data["grocery_list"]
            entry.title = form.cleaned_data["title"]
            entry.category = form.cleaned_data["category"]
            entry.quantity = form.cleaned_data["quantity"]
            entry.save()
            return HttpResponseRedirect("/")

        return self.get(request, entry_id)


class NewListView(TemplateView):
    template_name = "main/new_list.html"
    form_class = ListForm
    toolbarTitle = _("New Grocery List")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,
                      {"form": form,
                       'toolbarTitle': self.toolbarTitle})

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = request.user.id
            title = form.cleaned_data["title"]
            list = List(user=user, title=title)
            list.save()
            return HttpResponseRedirect("/")
        return self.get(request)


class NewEntryView(TemplateView):
    template_name = "main/new_entry.html"
    form_class = EntryForm
    toolbarTitle = _("New Entry")

    def get(self, request, list_id):
        form = self.form_class()

        return render(request, self.template_name,
                      {"form": form,
                       "toolbarTitle": self.toolbarTitle})

    def post(self, request, list_id, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            quantity = form.cleaned_data["quantity"]
            grocery_list = List.objects.get(id=list_id)
            next = "/list/{}".format(list_id)
            try:
                oldEntry = get_object_or_404(
                    Entry, title=title,
                    grocery_list=grocery_list,
                    category=category)
                if oldEntry:
                    oldQuantity = oldEntry.quantity
                    if quantity:
                        oldEntry.quantity = oldQuantity + quantity
                        oldEntry.save()
                    else:
                        return HttpResponseRedirect(next)
            except Http404:
                entry = Entry(title=title,
                              category=category,
                              quantity=quantity,
                              grocery_list=grocery_list)
                entry.save()
                return HttpResponseRedirect(next)
        return self.get(request, list_id)
