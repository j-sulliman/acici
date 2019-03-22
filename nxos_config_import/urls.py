from django.conf.urls import url

from .views import vlans_data, epgs_data, epg_new, epgs_form_data, object_config_data

from django.conf.urls import include
from django.urls import path
app_name = 'nxos_config_import'

urlpatterns = [
    url(r'^vlans/', vlans_data),
    url(r'^epgs/', epgs_data),
    url(r'^epgs_form/', epgs_form_data),
    url(r'^home/', epg_new),
    url(r'^configuration/', object_config_data),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
