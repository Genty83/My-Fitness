from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Attributes:
        Meta: Defines model and fields to exclude.
        __init__: Initializes form, adds placeholders and classes,
                  removes auto-generated labels, and sets autofocus
                  on the first field.
    """

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.

        Adds placeholders and CSS classes to the fields, removes 
        auto-generated labels, and sets autofocus on the first field.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_country': 'Country',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County',
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

        # Adding aria-labelledby for accessibility
        aria_ids = {
            'default_phone_number': 'phone-label',
            'default_country': 'country-label',
            'default_postcode': 'postcode-label',
            'default_town_or_city': 'town-label',
            'default_street_address1': 'address1-label',
            'default_street_address2': 'address2-label',
            'default_county': 'county-label',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = f'{placeholders[field]}{" *" if self.fields[field].required else ""}'
            self.fields[field].widget.attrs.update({
                'placeholder': placeholder,
                'class': ' '.join(classes),
                'aria-labelledby': aria_ids[field],
            })
            self.fields[field].label = False
