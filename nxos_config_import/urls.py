from django.conf.urls import url

from .views import vlans_data

from django.conf.urls import include
from django.urls import path
app_name = 'nxos_config_import'

urlpatterns = [
    url(r'^vlans/', vlans_data),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
