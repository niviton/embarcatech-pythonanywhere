from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('api/reservatorio/', views.reservatorio),
    path('api/controle-irrigacao/', views.controle_irrigacao),
    path('api/status-irrigacao/', views.status_irrigacao),
]



