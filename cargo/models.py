from django.db import models
from django.urls import reverse #Used to generate urls by reversing the URL patterns
from address.models import AddressField
from django.contrib.auth.models import User
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
    name = models.CharField(max_length=200, help_text="Enter the name for the facility (e.g. main office, storage 23, etc.)")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, help_text="Select the company this facility belongs to")
    address = AddressField()
    phone = PhoneNumberField(blank=True, help_text="Enter the facility contact number (e.g. +19999999999, etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Person(models.Model):
    """
    Model representing a Person (e.g. Lolo Perez, etc.)
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    cell = PhoneNumberField(blank=True, help_text="Enter the person contact number (e.g. +19999999999, etc.)")
    confirmed_phone = models.BooleanField(default=False)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.user.get_full_name()


class Employee(models.Model):
    """
    Model representing an Employee (e.g. Lolo Perez, dispatcher at Galianos Corp.)
    """
    person = models.ForeignKey(Person, on_delete=models.PROTECT, help_text="Select the person this employee represents")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, help_text="Select the company this employee works in")
    role = models.ManyToManyField(EmployeeRole, on_delete=models.PROTECT, help_text="Select the roles this employee have in the company")

    class Meta:
        ordering = ["company","person"]
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
        return '{0} ({1})'.format(self.user.get_full_name(), self.company.name) 


class Cargo(models.Model):
    """
    Model representing a Cargo or Load (e.g. Shipment x from  Broker y)
    """
    description = models.CharField(max_length=200, help_text="Enter a description for the cargo")
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    broker = models.ForeignKey(Employee, on_delete=models.PROTECT, help_text="Represents the employee from a brokerage company posting the cargo")
    posted = models.DateTimeField(auto_now_add=True, blank=False, help_text="Represents a timestamp of when the cargo was posted" )
    
    CARGO_STATUS = (
        ('p', 'Posted'),
        ('n', 'Negotiated'),
        ('a', 'Assigned'),
        ('o', 'On route'),
        ('d', 'Delivered'),
    )

    status= models.CharField(max_length=1, choices=CARGO_STATUS, default='p', help_text='Cargo status')

    dispatcher = models.ForeignKey(Employee, on_delete=models.PROTECT, help_text="Represents the employee from a carrier company who close the deal with the broker")
    negotiated = models.DateTimeField(blank=True, help_text="Represents a timestamp of when the cargo was negotiated with the broker" )
    
    driver = models.ForeignKey(Employee, on_delete=models.PROTECT, help_text="Represents the employee from a carrier company who was assigned for delivering the cargo")
    assigned = models.DateTimeField(blank=True, help_text="Represents a timestamp of when the cargo was assigned to the driver" )
    
    delivered = models.DateTimeField(blank=True, help_text="Represents a timestamp of when the cargo was delivered" )

    class Meta:
        ordering = ['-posted','description']

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
    

class Lumper(models.Model):


class Advancement(models.Model):


class Check(models.Model):





class PickupOrder(models.Model):

