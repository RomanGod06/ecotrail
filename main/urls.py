from django.urls import path
from . import views

# These 'name' parameters are CRITICAL. 
# They must perfectly match the {% url 'name' %} tags used in your base.html!
urlpatterns = [
    path('', views.home, name='home'),

    #path('', views.  , name = ''),
    path('impact/', views.impact  , name = 'impact'),
    path('ranking/', views.ranking  , name = 'ranking'),
    path('sos/', views.sos  , name = 'sos'),
    path('working/', views.working  , name = 'working'),
    path('about/', views.about  , name ='about'),
    path('map/', views.map, name='map'),
]

