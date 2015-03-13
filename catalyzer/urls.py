from django.conf.urls import patterns, include, url
from django.contrib import admin
from catalyzer import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'catalyzer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^$', 'dicom.views.view_files', name="view_files"),
    url(r'^upload$', 'dicom.views.upload'),
    
    url(r'^getdata$', 'dicom.views.view_data_api'),
    url(r'^download$', 'dicom.views.download_zip'),

    url(r'^admin/', include(admin.site.urls)),
    
)