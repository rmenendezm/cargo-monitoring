from django.urls import path
from cargo import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cargos/', views.CargoListView.as_view(), name='cargos'),
    path('cargo/<int:pk>', views.CargoDetailView.as_view(), name='cargo-detail'),
    path('cargos-available/', views.CargoAvailableListView.as_view(), name='cargos-available'),
    path('brokers/', views.BrokerListView.as_view(), name='brokers'),
    path('carriers/', views.CarrierListView.as_view(), name='carriers'),
    path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company-detail'),
    path('employees/', views.EmployeesByCompanyListView.as_view(), name='employees-by-company'),
    path('add-employee/', views.CreateEmployeeView.as_view(), name='add-employee'),
]