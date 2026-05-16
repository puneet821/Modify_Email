from django.db import models
from django.utils import timezone


class Email(models.Model):
    """A self-addressed email with a user-settable received date."""

    sender = models.CharField(
        max_length=255,
        default='',
        blank=True,
        help_text='Sender name displayed in inbox',
    )
    sender_email = models.EmailField(
        max_length=255,
        default='sender@example.com',
        help_text='Sender email address',
    )
    recipient = models.EmailField(
        max_length=255,
        default='me@gmail.com',
        help_text='Recipient (always yourself)',
    )
    subject = models.CharField(
        max_length=500,
        blank=True,
        default='',
    )
    body = models.TextField(blank=True, default='')
    received_date = models.DateTimeField(
        help_text='The date shown as "received" in the inbox (user-settable)',
    )
    is_read = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    
    FOLDER_CHOICES = [
        ('inbox', 'Inbox'),
        ('sent', 'Sent'),
        ('drafts', 'Drafts'),
        ('trash', 'Trash'),
    ]
    folder = models.CharField(
        max_length=10,
        choices=FOLDER_CHOICES,
        default='inbox',
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_date']

    def __str__(self):
        return f"{self.subject} — {self.received_date:%b %d, %Y %I:%M %p}"

    @property
    def snippet(self):
        """Return first 100 chars of body for inbox preview."""
        return self.body[:100] + ('…' if len(self.body) > 100 else '')


class Attachment(models.Model):
    """File attachment for an email."""
    email = models.ForeignKey(
        Email, related_name='attachments', on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.email.subject})"
