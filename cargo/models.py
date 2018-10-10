from django.db import models
from django.urls import reverse #Used to generate urls by reversing the URL patterns
from address.models import AddressField
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class EmployeeRole(models.Model):
    """
    Model representing an employee role (e.g. broker, dispatcher, driver, manager,owner).
    """
    role = models.CharField(max_length=200, unique=True, help_text="Enter an employee role (e.g. broker, dispatcher, driver, manager, owner)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.role
        
        
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
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
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
    person = models.OneToOneField(Person, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, help_text="Select the company this employee works in")
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, help_text="Select the role this employee have in the company"
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.user.get_full_name()

class Lumper(models.Model):


class Advancement(models.Model):


class Check(models.Model):


class Cargo(models.Model):


class PickupOrder(models.Model):

    
# class Book(models.Model):
#     """
#     Model representing a book (but not a specific copy of a book).
#     """
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
#       # Foreign Key used because book can only have one author, but authors can have multiple books
#       # Author as a string rather than object because it hasn't been declared yet in file.
#     summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
#     isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
#     genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
#       # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
#       # Genre class has already been defined so we can specify the object above.
#     language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
      
#     def display_genre(self):
#         """
#         Creates a string for the Genre. This is required to display genre in Admin.
#         """
#         return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
#         display_genre.short_description = 'Genre'
    
    
#     def get_absolute_url(self):
#         """
#         Returns the url to access a particular book instance.
#         """
#         return reverse('book-detail', args=[str(self.id)])

#     def __str__(self):
#         """
#         String for representing the Model object.
#         """
#         return self.title
        
        
# import uuid # Required for unique book instances
# from datetime import date

# from django.contrib.auth.models import User #Required to assign User as a borrower

# class BookInstance(models.Model):
#     """
#     Model representing a specific copy of a book (i.e. that can be borrowed from the library).
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
#     book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
#     imprint = models.CharField(max_length=200)
#     due_back = models.DateField(null=True, blank=True)
#     borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
#     @property
#     def is_overdue(self):
#         if self.due_back and date.today() > self.due_back:
#             return True
#         return False
        

#     LOAN_STATUS = (
#         ('d', 'Maintenance'),
#         ('o', 'On loan'),
#         ('a', 'Available'),
#         ('r', 'Reserved'),
#     )

#     status= models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')

#     class Meta:
#         ordering = ["due_back"]
#         permissions = (("can_mark_returned", "Set book as returned"),)   

#     def __str__(self):
#         """
#         String for representing the Model object.
#         """
#         #return '%s (%s)' % (self.id,self.book.title)
#         return '{0} ({1})'.format(self.id,self.book.title)
        

# class Author(models.Model):
#     """
#     Model representing an author.
#     """
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     date_of_death = models.DateField('died', null=True, blank=True)

#     class Meta:
#         ordering = ["last_name","first_name"]
    
#     def get_absolute_url(self):
#         """
#         Returns the url to access a particular author instance.
#         """
#         return reverse('author-detail', args=[str(self.id)])
    

#     def __str__(self):
#         """
#         String for representing the Model object.
#         """
#         return '{0}, {1}'.format(self.last_name,self.first_name)