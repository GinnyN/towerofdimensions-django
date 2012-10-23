from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', direct_to_template, {'template': 'index.html'}),
     url(r'^game/$', 'towerofdimensions.views.info'),
     
     #Log out
     url(r'^logout/$',  'django.contrib.auth.views.logout', {'next_page': '/'}),

     url(r'^mercenaries/$', 'towerofdimensions.mercenaries.setup'),
     url(r'^mercenaries/(?P<mercenary_id>\d+)/$', "towerofdimensions.mercenaries.fullView"),

   	url(r'', include('social_auth.urls')),



   	#url(r'^openid/', include('django_openid_auth.urls')),
    #url(r'^logout/$', 'django.contrib.auth.views.logout'),

    # Examples:
    # url(r'^$', 'ifz.views.home', name='home'),
    # url(r'^ifz/', include('ifz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
