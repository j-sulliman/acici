from django.conf.urls import url

from .views import vlans_data, epgs_data, epg_new, epgs_form_data, object_config_data, model_form_upload
from .views import simple_upload

from django.conf.urls import include
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'nxos_config_import'

urlpatterns = [
    url(r'^vlans/', vlans_data),
    url(r'^epgs/', epgs_data, name='epg-data'),
    url(r'^epgs_form/', epgs_form_data),
    url(r'^home/', epg_new, name='nci-home'),
    url(r'^configuration/', object_config_data),
    url(r'^model_form_upload/', model_form_upload),
    url(r'^simple/$', simple_upload, name='simple_upload'),
    url(r'^form/$', model_form_upload, name='model_form_upload')
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

