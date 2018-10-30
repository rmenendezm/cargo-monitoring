from django.contrib import admin

# Register your models here.

from cargo.models import CompanyType, Company, Facility, Employee, Cargo, PickupOrder, Lumper


admin.site.register(CompanyType)
admin.site.register(Company)
admin.site.register(Facility)
admin.site.register(Employee)
admin.site.register(Cargo)
admin.site.register(PickupOrder)
admin.site.register(Lumper)