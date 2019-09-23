from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    path(r'^delete/<list_id>', views.delete, name='delete'),
    path(r'^cross_off/<list_id>', views.cross_off, name='cross_off'),
    path(r'^uncross/<list_id>', views.uncross, name='uncross'),
    path(r'^edit/<list_id>', views.edit, name='edit'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

]