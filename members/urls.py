from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('search/', views.search, name='members'),
    path('game/', views.game, name='members'),
]