from django.urls import path
from . import views

# These 'name' parameters are CRITICAL. 
# They must perfectly match the {% url 'name' %} tags used in your base.html!
urlpatterns = [
    path('', views.home, name='home'),
<<<<<<< HEAD
    #path('', views.  , name = ''),
    path('impact/', views.impact  , name = 'impact'),
    path('ranking/', views.ranking  , name = 'ranking'),
    path('sos/', views.sos  , name = 'sos'),
    path('working/', views.working  , name = 'working'),
    path('about/', views.about  , name ='about'),
    path('map/', views.map , name='map'),
=======
    path('working/', views.working, name='working'),
    path('impact/', views.impact, name='impact'),
    path('about/', views.about, name='about'),
    path('ranking/', views.ranking, name='ranking'),
    path('sos/', views.sos, name='sos'),
>>>>>>> e8142840262f1fa5269846e218987075ccae89fb
]

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
    path('working/', TemplateView.as_view(template_name='main/working.html'), name='working'),
    path('impact/', TemplateView.as_view(template_name='main/impact.html'), name='impact'),
    path('about/', TemplateView.as_view(template_name='main/about.html'), name='about'),
    path('ranking/', TemplateView.as_view(template_name='main/ranking.html'), name='ranking'),
    path('sos/', TemplateView.as_view(template_name='main/sos.html'), name='sos'),
]