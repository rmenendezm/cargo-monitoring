from django.contrib import admin

# Register your models here.

from cargo.models import EmployeeRole, CompanyType, Company, Facility, Person, Employee, Cargo, PickupOrder, Lumper

admin.site.register(EmployeeRole)
admin.site.register(CompanyType)
admin.site.register(Company)
admin.site.register(Facility)
admin.site.register(Person)
admin.site.register(Employee)
admin.site.register(Cargo)
admin.site.register(PickupOrder)
admin.site.register(Lumper)