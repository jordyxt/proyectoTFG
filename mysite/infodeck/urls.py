from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
 path('', views.index, name='index'),
 path('about/', views.about, name='about'),
 path('search', views.search, name='search'),
 url(r'^', include(router.urls)),
 url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
 url(r'^api/deck/(?P<pk>[0-9]+)/$', views.deck_detail),
]
