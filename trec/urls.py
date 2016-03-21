from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^main/', include('main.urls')),
    url(r'^$', RedirectView.as_view(url="/main/", permanent=True), name='rootNoparams'),)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_PATH)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
