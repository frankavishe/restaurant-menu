import re

from django import forms

from .models import ContactMessage

# Light email-or-phone check: accepts a standard email address, or a phone
# number consisting of digits and common separators (+, spaces, dashes,
# parentheses) with at least 7 digits.
EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
PHONE_PATTERN = re.compile(r'^\+?[\d\s\-()]{7,}$')


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'contact_info', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'maxlength': 2000, 'rows': 5}),
        }

    def clean_contact_info(self):
        contact_info = self.cleaned_data['contact_info'].strip()
        if not (EMAIL_PATTERN.match(contact_info) or PHONE_PATTERN.match(contact_info)):
            raise forms.ValidationError(
                'Enter a valid email address or phone number.'
            )
        return contact_info
