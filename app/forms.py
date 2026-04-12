from django import forms
from .models import Email


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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

    attachments = MultipleFileField(
        required=False,
        label='Attachments',
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
