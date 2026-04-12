from django import forms
from .models import Email


class ComposeEmailForm(forms.ModelForm):
    """Form for composing a self-email with custom received date."""

    received_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-input',
                'id': 'received-date',
            }
        ),
        label='Received Date & Time',
        help_text='Set the date this email should appear as received',
    )

    class Meta:
        model = Email
        fields = ['sender', 'subject', 'body', 'received_date']
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Sender name (e.g. John Doe)',
                'id': 'sender',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject',
                'id': 'subject',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your email here...',
                'rows': 12,
                'id': 'body',
            }),
        }
