from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^$',views.index,name='index'),
    url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^edit_profile/$',views.edit_profile,name='edit_profile'),
    )