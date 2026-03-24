from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.  , name = ''),
    path('impact/', views.impact  , name = 'impact'),
    path('ranking/', views.ranking  , name = 'ranking'),
    path('sos/', views.sos  , name = 'sos'),
    path('working/', views.working  , name = 'working'),
    path('about/', views.about  , name ='about'),
]

