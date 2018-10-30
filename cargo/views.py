from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from cargo.models import Cargo, PickupOrder, Company, Employee
from cargo.forms import CreateEmployeeForm

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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    
    context = {
        'num_cargos': num_cargos,
        'num_pickuporders': num_pickuporders,
        'num_cargos_available': num_cargos_available,
        'num_brokerages': num_brokerages,
        'num_carriers': num_carriers,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class CargoListView(generic.ListView):
    model = Cargo
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CargoListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['page_title'] = 'Cargo List'
        return context


class CargoAvailableListView(CargoListView):
    queryset = Cargo.objects.filter(status__exact='p')[:15] # Get 15 available cargos 
    #template_name = 'cargo/cargo_available_list.html'  # Specify your own template name/location
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CargoAvailableListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['page_title'] = 'Available Cargo List'
        return context


class CompanyListlView(generic.ListView):
    model = Company
    paginate_by = 5

class BrokerListView(CompanyListlView):
    context_object_name = 'broker_list'   # your own name for the list as a template variable
    queryset = Company.objects.filter(type__type__iexact='brokerage')[:15] # Get 15 brokers 
    template_name = 'cargo/broker_list.html'  # Specify your own template name/location


class CarrierListView(CompanyListlView):
    context_object_name = 'carrier_list'   # your own name for the list as a template variable
    queryset = Company.objects.filter(type__type__iexact='carrier')[:15] # Get 15 carriers
    template_name = 'cargo/carrier_list.html'  # Specify your own template name/location


class CargoDetailView(generic.DetailView):
    model = Cargo

class CompanyDetailView(generic.DetailView):
    model = Company


# class CargosPostedByBrokerageListView(LoginRequiredMixin,generic.ListView):
#     """Generic class-based view listing books on loan to current user."""
#     model = Cargo
#     template_name ='cargo/cargos_posted_by_broker.html'
#     paginate_by = 10
    
#     def get_queryset(self):
#         return Cargo.objects.filter(broker=self.request.user).filter(status__exact='p').order_by('-posted')


class EmployeesByCompanyListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Employee
    template_name ='cargo/employee_list_by_company.html'
    paginate_by = 10
    permission_required = ('cargo.view_employee')
    
    def get_queryset(self):
        the_employee = Employee.objects.get(user=self.request.user)
        the_company  = Company.objects.get(pk=the_employee.company.id)
        return Employee.objects.filter(company=the_company)


class CreateEmployeeView(PermissionRequiredMixin, generic.CreateView):
    #login_url = reverse_lazy('users:login')
    form_class          = CreateEmployeeForm
    template_name       = 'cargo/employee_create.html'
    permission_required = ('cargo.add_employee')
    success_url         = reverse_lazy('employees-by-company')
    success_message     = 'New employee has been created. The password has been emailed to the employee email address.'
    
    def get_form_kwargs(self):
        kwargs = super(CreateEmployeeView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        cxt   = {'form': form, }
        user  = form.save(commit=False)
        # Cleaned(normalized) data
        phone = form.cleaned_data['phone']
        # password = form.cleaned_data['password']
        # repeat_password = form.cleaned_data['repeat_password']
        # if password != repeat_password:
        #     messages.error(self.request, "Passwords do not Match", extra_tags='alert alert-danger')
        #     return render(self.request, self.template_name, cxt)
        user.set_password('w12sdQd!')
        user.save()
 
        # Create Employee model
        manager  = Employee.objects.get(user=self.request.user)
        the_company  = Company.objects.get(pk=manager.company.id)
        Employee.objects.create(user=user, phone=phone, company=the_company)
 
        return super(CreateEmployeeView, self).form_valid(form)