from django.urls import path
from cargo import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cargos/', views.CargoListView.as_view(), name='cargos'),
    path('brokers/', views.BrokerListView.as_view(), name='brokers'),
    path('carriers/', views.CarrierListView.as_view(), name='carriers'),
]