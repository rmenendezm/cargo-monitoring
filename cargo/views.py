from django.shortcuts import render
from cargo.models import Cargo, PickupOrder, Company
from django.views import generic

# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_cargos = Cargo.objects.all().count()
    num_pickuporders = PickupOrder.objects.all().count()
    
    # Available books (status = 'a')
    num_cargos_available = Cargo.objects.filter(status__exact='p').count()
    
    # Amount of Brokerage companies (type = 'brokerage')
    # The 'all()' is implied by default.    
    num_brokerages = Company.objects.filter(type__type__iexact='brokerage').count()
    
    # Amount of Carriers companies (type = 'carrier')
    num_carriers = Company.objects.filter(type__type__iexact='carrier').count()
    
    context = {
        'num_cargos': num_cargos,
        'num_pickuporders': num_pickuporders,
        'num_cargos_available': num_cargos_available,
        'num_brokerages': num_brokerages,
        'num_carriers': num_carriers,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class CargoListView(generic.ListView):
    model = Cargo


class BrokerListView(generic.ListView):
    model = Company
    context_object_name = 'broker_list'   # your own name for the list as a template variable
    queryset = Company.objects.filter(type__type__iexact='brokerage')[:15] # Get 15 brokers 
    template_name = 'brokers/broker_list.html'  # Specify your own template name/location


class CarierListView(generic.ListView):
    model = Company
    context_object_name = 'carrier_list'   # your own name for the list as a template variable
    queryset = Company.objects.filter(type__type__iexact='carrier')[:15] # Get 15 carriers
    template_name = 'carriers/carrier_list.html'  # Specify your own template name/location

