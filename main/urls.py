from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/(?P<list_id>[\d])/$',
        views.show_list, name="show_list"),
    url(r'^list/new_list',
        login_required(views.NewListView.as_view()),
        name='new_list'),
    url(r'^list/(?P<list_id>[\d])/new_entry',
        login_required(views.NewEntryView.as_view()),
        name='new_entry'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'}, name="logout"),
]
