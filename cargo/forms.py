import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from phonenumber_field.formfields import PhoneNumberField
from cargo.models import Company, Employee

# class AddEmployeeForm(forms.Form):
#     username    = forms.CharField(min_length=4, max_length=254, strip=True, required=True, help_text="Enter a user name.")
#     password    = forms.CharField(label=_("Password"), widget=forms.PasswordInput, min_length=8, strip=True, required=True, help_text="Enter a password, min length 8 characters.")
#     re_password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, min_length=8, strip=True, required=True, help_text="Retype the password.")
#     first_name  = forms.CharField(max_length=50, strip=True, required=True, help_text="Enter the first name.")
#     last_name   = forms.CharField(max_length=50, strip=True, required=True, help_text="Enter the last name.")
#     email       = forms.EmailField(strip=True, required=True, help_text="Enter an email address.") 
#     phone       = forms.PhoneNumberField(help_text="Enter an email address.")
#     active
#     groups
#     company


#     renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

#     def clean_renewal_date(self):
#         data = self.cleaned_data['renewal_date']
        
#         # Check if a date is not in the past. 
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))

#         # Check if a date is in the allowed range (+4 weeks from today).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#         # Remember to always return the cleaned data.
#         return data


class CreateEmployeeForm(forms.ModelForm):
    phone   = PhoneNumberField()
    #phone   = PhoneNumberField(help_text="Enter a phone number.")
    
    # role    = forms.MultipleChoiceField(
    #             required=True,
    #             widget=forms.CheckboxSelectMultiple,
    #             choices=FAVORITE_COLORS_CHOICES,
    #           )

    role    = forms.ModelMultipleChoiceField(queryset = None)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole

        super(CreateEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Group.objects.all()
        # User.objects.filter(pk=self.user.id)
        #self.fields['role'].queryset = Employee.objects.filter(user=self.user).all()


        # # If the user does not belong to a certain group, remove the field
        # if not self.user.groups.filter(name__iexact='mygroup').exists():
        #     del self.fields['confidential']