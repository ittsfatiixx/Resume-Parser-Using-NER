from django.urls import path
from . import views
urlpatterns = [
    path('', views.topView, name='homeView'),
    path('all', views.allView, name='homeView'),
    path('rejected', views.rejectedView, name='homeView'),
]






