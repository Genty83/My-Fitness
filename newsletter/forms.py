from django import forms
from .models import Newsletters

class NewsletterForm(forms.ModelForm):
    """ Form for editing and creating newsletters """
    class Meta:
        model = Newsletters
        fields = [
            'title', 
            'content', 
            'is_published', 
            'date_published',
            'image',
            'image_url'
            ]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {  
            'title': 'Title',
            'content': 'Content',
            'is_published': 'Is Published',
            'date_published': 'Date Published',
            'image': 'Image',
            'image_url': 'Image URL'
        }
        
        classes = [
            'bg-slate-600',
            'bd-radius-1',
            'transition-fast',
            'shadow-focus-1',
            'sh-sky-300',
            'bd-width-0',
            'width-100',
            'pad-inline-1'
        ]

        self.fields['title'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ' '.join(classes)
            self.fields[field].label = False