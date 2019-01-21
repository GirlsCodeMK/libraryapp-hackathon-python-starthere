import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from library.models import Copy
    
class RenewLoanForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class ReturnLoanForm(forms.Form):
    return_date = forms.DateField(help_text="Enter the date of return.")

    def clean_return_date(self):
        data = self.cleaned_data['return_date']
        
        # Check if a date is not in the past. 
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - return in future'))

        # Remember to always return the cleaned data.
        return data

class IssueFindUserForm(forms.Form):
    selected_user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Library user').order_by('username')
        )


def get_copies():
    copy_choices = [(c.pk, str(c)) for c in Copy.objects.all() if c.available]
    return copy_choices
    # for province in ProvinceCode.objects.filter(country_code_id=1).order_by('code'):
    #     province_choices.append((province.code, province.code))
    # return province_choices

class IssueToUserForm(forms.Form):
    selected_copy = forms.ChoiceField(choices=get_copies)
    return_due = forms.DateField()

class BookSearchForm(forms.Form):

    q = forms.CharField(required=False)

    order_choices =[
        (1, "Author A-Z"), 
        (2, "Author Z-A"), 
        (3, "Title A-Z"),
        (4, "Title Z-A"),
        ]
    order = forms.ChoiceField(choices=order_choices, label='Sort order', 
        required=False, initial=3)
