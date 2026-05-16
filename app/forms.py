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

    confirm_sender_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Confirm sender email',
                'id': 'confirm-sender-email',
            }
        ),
        label='Confirm Sender Email',
        help_text='Re-type the sender email for confirmation',
    )

    def clean(self):
        cleaned_data = super().clean()
        sender_email = cleaned_data.get('sender_email')
        confirm_email = cleaned_data.get('confirm_sender_email')

        if sender_email and confirm_email and sender_email != confirm_email:
            self.add_error('confirm_sender_email', "Emails do not match.")
        
        return cleaned_data

    class Meta:
        model = Email
        fields = ['sender', 'sender_email', 'subject', 'body', 'received_date']
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Sender name (e.g. John Doe)',
                'id': 'sender',
            }),
            'sender_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Sender email (e.g. john@example.com)',
                'id': 'sender-email',
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
