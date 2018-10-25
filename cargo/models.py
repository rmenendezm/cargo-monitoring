from django.db import models
from django.urls import reverse #Used to generate urls by reversing the URL patterns
#from address.models import AddressField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

# Create your models here.


class EmployeeRole(models.Model):
    """
    Model representing an employee role (e.g. broker, dispatcher, driver, manager,owner).
    """
    name = models.CharField(max_length=200, unique=True, help_text="Enter an employee role (e.g. broker, dispatcher, driver, manager, owner)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
        
class CompanyType(models.Model):
    """
    Model representing a company's type (e.g. brokerage, carrier, sender/receiver)
    """
    type = models.CharField(max_length=200, unique=True, help_text="Enter the company's type (e.g. brokerage, carrier, sender/receiver)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.type
        
        
class Company(models.Model):
    """
    Model representing a Company (e.g. Galiano Corp, Bravo Supermarket, etc.)
    """
    name = models.CharField(max_length=200, unique=True, help_text="Enter the company's name (e.g. Galiano Corp, Bravo Supermarket, etc.)")
    type = models.ForeignKey(CompanyType, on_delete=models.PROTECT, help_text="Select a type for this company")
    
    class Meta:
        ordering = ['type', 'name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular company
        """
        return reverse('company-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Facility(models.Model):
    """
    Model representing a Facility (e.g. Bravo Supermarket Storage 23, etc.)
    """
    name    = models.CharField(max_length=200, help_text="Enter the name for the facility (e.g. main office, storage 23, etc.)")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, help_text="Select the company this facility belongs to")
    address = models.CharField(max_length=200, help_text="Enter the address of the facility")
    phone   = PhoneNumberField(blank=True, help_text="Enter the facility contact number (e.g. +19999999999, etc.)")

    class Meta:
        ordering = ['company', 'name']
        #permissions = (("can_edit_book", "Allowed to edit"),)    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular facility
        """
        return reverse('facility-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Person(models.Model):
    """
    Model representing a Person (e.g. Lolo Perez, etc.)
    """
    user           = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    cell           = PhoneNumberField(blank=True, help_text="Enter the person contact number (e.g. +19999999999, etc.)")
    cell_confirmed = models.BooleanField(default=False)

    def get_absolute_url(self):
        """
        Returns the url to access a particular person
        """
        return reverse('person-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return f'({self.user.username}) - {self.user.get_full_name()}'


class Employee(models.Model):
    """
    Model representing an Employee (e.g. Lolo Perez, dispatcher at Galianos Corp.)
    """
    person  = models.ForeignKey(Person, on_delete=models.PROTECT, help_text="Select the person this employee represents")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, help_text="Select the company this employee works in")
    role    = models.ManyToManyField(EmployeeRole, help_text="Select the roles this employee have in the company")

    class Meta:
        ordering = ['company', 'person']
        #permissions = (("can_edit_book", "Allowed to edit"),)   

    def display_role(self):
        """
        Creates a string for the Role. This is required to display role in Admin.
        """
        return ', '.join([ role.name for role in self.role.all()[:3] ])
        
    display_role.short_description = 'Role XXXX'

    def get_absolute_url(self):
        """
        Returns the url to access a particular employee
        """
        return reverse('employee-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '{0} ({1})'.format(self.person.user.get_full_name(), self.company.name) 


class Cargo(models.Model):
    """
    Model representing a Cargo or Load (e.g. Shipment x from  Broker y)
    """
    description = models.CharField(max_length=200, help_text="Enter a description for the cargo")
    price       = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    #broker      = models.ForeignKey(Employee, related_name='broker', on_delete=models.PROTECT, help_text="Represents the employee from a brokerage company posting the cargo")
    
    broker      = models.ForeignKey(User, related_name='broker', on_delete=models.PROTECT, help_text="Represents the employee from a brokerage company posting the cargo")
    posted      = models.DateTimeField(auto_now_add=True, blank=False, help_text="Represents a timestamp of when the cargo was posted" )
    
    CARGO_STATUS = (
        ('p', 'Posted'),
        ('n', 'Negotiated'),
        ('a', 'Assigned'),
        ('o', 'On route'),
        ('d', 'Delivered'),
    )

    status     = models.CharField(max_length=1, choices=CARGO_STATUS, default='p', help_text='Cargo status')

    dispatcher = models.ForeignKey(User, related_name='dispatcher', on_delete=models.PROTECT, blank=True, null=True, help_text="Represents the employee from a carrier company who close the deal with the broker")
    negotiated = models.DateTimeField(null=True, blank=True, help_text="Represents a timestamp of when the cargo was negotiated with the broker" )
    
    driver     = models.ForeignKey(User, related_name='driver', on_delete=models.PROTECT, blank=True, null=True, help_text="Represents the employee from a carrier company who was assigned for delivering the cargo")
    assigned   = models.DateTimeField(null=True, blank=True, help_text="Represents a timestamp of when the cargo was assigned to the driver" )
    
    delivered  = models.DateTimeField(null=True, blank=True, help_text="Represents a timestamp of when the cargo was delivered" )

    class Meta:
        ordering = ['-posted','description', '-price']

    def get_absolute_url(self):
        """
        Returns the url to access a particular cargo instance.
        """
        return reverse('cargo-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - {1} - {2} - {3}'.format(self.posted, self.description, self.price, self.broker.company.name) 
    

class PickupOrder(models.Model):
    """
    Model representing a Pickup Order (e.g. Pickup Order w for Shipment x)
    """
    cargo       = models.ForeignKey(Cargo, on_delete=models.PROTECT, help_text="Represents the load or cargo to which the pick order belongs to")
    pickup_from = models.ForeignKey(Facility, related_name='pickup_from', on_delete=models.PROTECT, help_text="Represents the facility where the cargo is collected")
    deliver_to  = models.ForeignKey(Facility, related_name='deliver_to', on_delete=models.PROTECT, help_text="Represents the facility where the cargo is delivered")

    bol_image   = models.ImageField(upload_to='bol_images', blank=True)
    pod_image   = models.ImageField(upload_to='pod_images', blank=True)

    loaded      = models.DateTimeField(blank=True, help_text="Represents a timestamp of when the cargo was loaded" )
    delivered   = models.DateTimeField(blank=True, help_text="Represents a timestamp of when the cargo was delivered" )

    class Meta:
        ordering = ['-cargo', 'pickup_from']

    def get_absolute_url(self):
        """
        Returns the url to access a particular capickup order.
        """
        return reverse('pickup-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}-{1} {2}'.format(self.cargo.id, self.id, self.pickup_from.name) 
    

class Lumper(models.Model):
    """
    Model representing a lumper for a specific pickup (e.g. Lumper z for Pickup Order w)
    """
    pickup_order = models.ForeignKey(PickupOrder, on_delete=models.PROTECT, help_text="Represents the pickup order to which the lumper was done")
    image        = models.ImageField(upload_to='lumper_images', blank=True)
    price        = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    requested    = models.DateTimeField(auto_now_add=True, blank=False, help_text="Represents a timestamp of when the lumper was requested" )

    paid      = models.DateTimeField(blank=True, help_text="Represents a timestamp of when the lumper was payed (e.g. Electronic check received" )
        
    class Meta:
        ordering = ['-requested']

    def get_absolute_url(self):
        """
        Returns the url to access a particular lumper for a pickup order.
        """
        return reverse('lumper-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}-{1}-{2} {3}'.format(self.pickup_order.cargo.id, self.pickup_order.id, self.id, self.price) 


# class Advancement(models.Model):


# class Check(models.Model):







