from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from .models import List, Entry
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from .forms import ListForm, EntryForm
from collections import OrderedDict
from django.views.decorators.csrf import csrf_protect


@login_required
def index(request):
    toolbarTitle = _("All Grocery Lists")
    user = request.user.id
    lists = List.objects.all().filter(user=user)
    return render(request, "main/index.html",
                  {"toolbarTitle": toolbarTitle,
                   "lists": lists})


@login_required
def change_list_title(request, list_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        _list = List.objects.get(id=list_id)
        _list.title = title
        _list.save()
        data = {
            'title': title
        }
        return JsonResponse(data)
    else:
        return JsonResponse({})


@login_required
def delete_list(request, list_id):
    if request.method == 'POST':
        List.objects.get(id=list_id).delete()
        data = {
        }
        return JsonResponse(data)
    else:
        return JsonResponse({})


@login_required
def delete_entry(request, list_id, entry_id):
    print("test")
    if request.method == 'POST':
        Entry.objects.filter(grocery_list=list_id).filter(id=entry_id).delete()
        data = {
        }
        return JsonResponse(data)
    else:
        return JsonResponse({})
    

@login_required
def validate_entry(request, list_id):
    title = request.GET.get('title')
    data = {
        'is_taken': Entry.objects
        .filter(grocery_list=list_id)
        .filter(title=title).exists(),
        'error_message': _('An entry with this title was already created in this list.')
    }
    return JsonResponse(data)


class ShowListView(TemplateView):
    template_name = "main/show_list.html"
    form_class = ListForm

    def get(self, request, list_id):
        _list = get_object_or_404(List, id=list_id)
        form = ListForm(request.POST or None, instance=_list)
        entries = Entry.objects.filter(grocery_list=list_id)
        entries_categories = Entry.objects.filter(grocery_list=list_id)
        if _list.order is None:
            entries = entries.order_by('category')
        entries_categories = dict((_.category, _) for _ in entries_categories)
        return render(request, self.template_name,
                      {"toolbarTitle": _list.title,
                       "entries": entries,
                       'list_id': list_id,
                       'form': form,
                       'entries_categories': entries_categories})

    def post(self, request, list_id, *args, **kwargs):
        _list = List.objects.get(id=list_id)

        categories = OrderedDict(Entry.objects.filter(
            grocery_list=list_id).values_list('id', 'category'))

        _list.order = ''.join(request.POST.getlist('order[]'))
        # get the order list from the database
        order_list = [_list.order[i:i + 2]
                      for i in range(0, len(_list.order), 2)]

        # for better performance?
        index_map = {v: i for i, v in enumerate(order_list)}

        none_order_list = []
        # handle None values
        for key in list(categories.keys()):
            if categories[key] is None:
                none_order_list.append(key)
                del categories[key]

        new_entry_order = sorted(
            categories.items(), key=lambda pair: index_map[pair[1]])
        new_entry_order = [x[0] for x in new_entry_order]
        new_entry_order.extend(none_order_list)

        _list.set_entry_order(new_entry_order)
        _list.save()

        return self.get(request, list_id)


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

    def get(self, request, list_id, entry_id):
        entry = get_object_or_404(Entry, id=entry_id)
        form = EntryForm(instance=entry)
        return render(request, self.template_name,
                      {"form": form,
                       'toolbarTitle': self.toolbarTitle,
                       'entry': entry.title,
                       'list_id': list_id,
                       'entry_id': entry_id})

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
            if Entry.objects.filter(title=title):
                return self.get(request, list_id)
            category = form.cleaned_data["category"]
            quantity = form.cleaned_data["quantity"]
            grocery_list = List.objects.get(id=list_id)
            next = "/list/{}".format(list_id)
            entry = Entry(title=title,
                          category=category,
                          quantity=quantity,
                          grocery_list=grocery_list)
            entry.save()
            return HttpResponseRedirect(next)
        return self.get(request, list_id)
