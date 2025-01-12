from django.urls import path
from . import views


urlpatterns = [
  path('', views.home),
  path('write/', views.write, name='write'),
  path('new_person/', views.new_person, name='new_person'),
  path('read/', views.read, name='read'),
  path('delete/', views.delete, name='delete'),
]
