"""
Forms for managing products in the application.
"""

from django import forms
from .models import Product, Category, SubCategory

# Add product form
class ProductForm(forms.ModelForm):
    """
    Form for adding a new product.
    """
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with category and subcategory choices.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        category_ids = [(int(c.id), c.get_friendly_name()) for c in categories]
        subcategory_ids = [(int(s.id), s.get_friendly_name()) for s in sub_categories]

        classes = [
            'bg-slate-600',
            'bd-radius-1',
            'bd-width-0',
            'shadow-focus-1',
            'transition-fast',
            'sh-sky-300'
        ]

        self.fields['category_id'].choices = category_ids
        self.fields['subcategory_id'].choices = subcategory_ids
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ' '.join(classes)


# Update product form
class UpdateProductForm(forms.ModelForm):
    """
    Form for updating an existing product.
    """
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['slug', 'date_added']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with category and subcategory choices.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        category_ids = [(int(c.id), c.get_friendly_name()) for c in categories]
        subcategory_ids = [(int(s.id), s.get_friendly_name()) for s in sub_categories]

        self.fields['category_id'].choices = category_ids
        self.fields['subcategory_id'].choices = subcategory_ids
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'