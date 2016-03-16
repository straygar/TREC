from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^edit_profile/$',views.edit_profile,name='edit_profile'),
    url(r'^about/$',views.about,name='about'),
    url(r'^run/new/', views.uploadRun, name="new_run"),
    url(r'^task/new/', views.uploadTask, name="new_task"),
    url(r'^track/new/', views.uploadTrack, name="new_track"),
    url(r'^genre/new/', views.uploadGenre, name="new_genre"),
    url(r'^browse/$', views.browse, name='browse'),
    )