from django.urls import path
from cargo import views


urlpatterns = [
    path('', views.index, name='index'),
]