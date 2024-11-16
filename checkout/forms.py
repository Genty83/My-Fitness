from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 
            'email', 
            'phone_number',
            'postcode',
            'town_or_city', 
            'street_address1',
            'street_address2',
            'country', 
            'county')
        
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels
        and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality'
        }

        classes = [
            'bg-slate-600',
            'bd-radius-1',
            'bd-width-0',
            'shadow-focus-1',
            'transition-fast',
            'sh-sky-300',
            'ft-serif',
            'pad-inline-1'
        ]
        
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ' '.join(classes)
            self.fields[field].label = False
