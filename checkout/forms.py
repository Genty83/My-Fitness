from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form for placing an order. This form handles input for the customer's 
    name, email, phone number, address, and other relevant details.
    """

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
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the order form with custom placeholders, CSS classes, 
        and ARIA attributes for improved accessibility. Autofocus is set 
        on the first field.
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
            'county': 'County, State or Locality',
        }

        classes = [
            'bg-slate-600',
            'bd-radius-1',
            'bd-width-0',
            'shadow-focus-1',
            'transition-fast',
            'sh-sky-300',
            'ft-serif',
            'pad-inline-1',
        ]

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs.update({
                'placeholder': placeholder,
                'class': ' '.join(classes),
                'aria-label': placeholders[field]
            })
            self.fields[field].label = False
