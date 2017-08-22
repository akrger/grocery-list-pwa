from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

# TODO change edit entry and add list_id to url
urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/(?P<list_id>[\d]+)/$',
        login_required(views.ShowListView.as_view()), name="show_list"),
    url(r'^list/(?P<list_id>[\d]+)/change_list_title/$',
        views.change_list_title, name="change_list_title"),
    url(r'^list/(?P<list_id>[\d]+)/delete_list/$',
        views.delete_list, name="delete_list"),
    url(r'^list/(?P<list_id>[\d]+)/delete_entry/(?P<entry_id>[\d]+)/$',
        views.delete_entry, name="delete_entry"),
    url(r'^list/(?P<list_id>[\d]+)/validate_entry/$',
        views.validate_entry, name="validate_entry"),
    url(r'^list/new_list',
        login_required(views.NewListView.as_view()),
        name='new_list'),
    url(r'^list/(?P<list_id>[\d]+)/new_entry',
        login_required(views.NewEntryView.as_view()),
        name='new_entry'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'}, name="logout"),
    url(r'^list/all', views.show_all_entries, name="show_all_entries"),
    url(r'^list/(?P<list_id>[\d]+)/edit_entry/(?P<entry_id>[\d]+)/$',
        login_required(views.EditEntryView.as_view()),
        name='edit_entry'),
]
