from django import forms
from .models import ProductReview 

class ProductReviewForm(forms.ModelForm):
    """
    A form for submitting product reviews, including a text review and a rating.
    """

    class Meta:
        """
        Meta options for the ProductReviewForm.
        Specifies the model and fields to include in the form.
        """
        model = ProductReview
        fields = ['title', 'review', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'review': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.1}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom attributes and placeholders for the fields.
        """
        super().__init__(*args, **kwargs)
        
        classes = [
            'bg-slate-600',
            'bd-radius-1',
            'transition-fast',
            'shadow-focus-1',
            'sh-sky-300',
            'bd-width-0',
            'width-100',
            'pad-inline-1',
            'ft-serif'
        ]
        
        self.fields['title'].label = 'Title'
        self.fields['review'].label = 'Review'
        self.fields['rating'].label = 'Rating'
        self.fields['title'].widget.attrs['placeholder'] = 'Title...'
        self.fields['review'].widget.attrs['placeholder'] = 'Write your review here...'
        self.fields['rating'].widget.attrs['placeholder'] = 'Rating (1-5)'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ' '.join(classes)
            field.label = False