from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/(?P<list_id>[\d])/$',
        login_required(views.ShowListView.as_view()), name="show_list"),
    url(r'^list/new_list',
        login_required(views.NewListView.as_view()),
        name='new_list'),
    url(r'^list/(?P<list_id>[\d])/new_entry',
        login_required(views.NewEntryView.as_view()),
        name='new_entry'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'}, name="logout"),
    url(r'^list/all', views.show_all_entries, name="show_all_entries"),
    url(r'^list/edit_entry/(?P<entry_id>[\d])/$',
        login_required(views.EditEntryView.as_view()),
        name='edit_entry'),
]
