from django.shortcuts import render
from django.http import HttpResponseRedirect
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


@login_required
def show_list(request, list_id):
    list_title = List.objects.get(id=list_id).title
    entries = Entry.objects.all().filter(grocery_list=list_id)
    return render(request, "main/show_list.html",
                  {"toolbarTitle": list_title,
                   "entries": entries,
                   'list_id': list_id})


class NewListView(TemplateView):
    template_name = "main/new_list.html"
    form_class = ListForm
    toolbarTitle = _("New Grocery List")

    def get(self, request):
        form = self.form_class()
        return render(request, "main/new_list.html",
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
        return render(request, self.template_name, {"form": form})


class NewEntryView(TemplateView):
    template_name = "main/new_entry.html"
    form_class = EntryForm
    toolbarTitle = _("New Entry")

    def get(self, request, list_id):
        form = self.form_class()

        return render(request, "main/new_entry.html",
                      {"form": form,
                       "toolbarTitle": self.toolbarTitle})

    def post(self, request, list_id, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            quantity = form.cleaned_data["quantity"]
            grocery_list = List.objects.get(id=list_id)
            entry = Entry(title=title, quantity=quantity,
                          grocery_list=grocery_list)
            entry.save()
            next = "/list/{}".format(list_id)
            return HttpResponseRedirect(next)
        return render(request, self.template_name, {"form": form})
