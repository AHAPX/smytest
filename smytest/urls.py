from django.conf.urls import patterns, include, url
from django.contrib import admin
from smytest.views import MainViewSet, indexView


urlpatterns = patterns('',
    url(r'^api/models/', MainViewSet.as_view({'get': 'get_models'}), name = 'models_list'),
    url(r'^api/model/', MainViewSet.as_view({'post': 'get_model'}), name = 'model'),
    url(r'^api/add/', MainViewSet.as_view({'post': 'add_new'}), name = 'add'),
    url(r'^api/modify/', MainViewSet.as_view({'post': 'modify'}), name = 'modify'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', indexView, name = 'home'),
)
