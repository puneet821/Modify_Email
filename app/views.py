from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Email, Attachment
from .forms import ComposeEmailForm


def inbox(request, folder='inbox'):
    """Display emails in the specified folder, newest (by received_date) first.
    
    Special folder 'starred' filters all emails where is_starred=True.
    """
    query = request.GET.get('q', '')
    
    if folder == 'starred':
        emails = Email.objects.filter(is_starred=True).exclude(folder='trash')
    else:
        emails = Email.objects.filter(folder=folder)

    if query:
        emails = emails.filter(
            models.Q(subject__icontains=query) | 
            models.Q(body__icontains=query) | 
            models.Q(sender__icontains=query)
        )

    context = {
        'emails': emails,
        'query': query,
        'current_folder': folder,
        'total_count': Email.objects.count(),
        'unread_count': Email.objects.filter(is_read=False, folder='inbox').count(),
    }
    return render(request, 'inbox.html', context)


def compose(request):
    """Compose and send a new self-email."""
    if request.method == 'POST':
        form = ComposeEmailForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.save(commit=False)
            if not email.sender.strip():
                email.sender = 'me'
            if not email.subject.strip():
                email.subject = '(no subject)'
            
            # Determine folder (Drafts or Inbox)
            if 'save_draft' in request.POST:
                email.folder = 'drafts'
                success_msg = 'Draft saved.'
            else:
                email.folder = 'inbox'
                success_msg = f'Email "{email.subject}" delivered to inbox!'
                
            email.save()

            # Handle attachments
            files = request.FILES.getlist('attachments')
            for f in files:
                Attachment.objects.create(
                    email=email,
                    file=f,
                    filename=f.name,
                    file_size=f.size
                )

            messages.success(request, success_msg)
            return redirect('app:inbox')
    else:
        form = ComposeEmailForm()

    context = {
        'form': form,
        'unread_count': Email.objects.filter(is_read=False, folder='inbox').count(),
    }
    return render(request, 'compose.html', context)


def email_detail(request, pk):
    """View a single email and mark it as read."""
    email = get_object_or_404(Email, pk=pk)
    if not email.is_read:
        email.is_read = True
        email.save(update_fields=['is_read'])
    return render(request, 'email_detail.html', {
        'email': email,
        'unread_count': Email.objects.filter(is_read=False, folder='inbox').count(),
    })


def toggle_star(request, pk):
    """Toggle the starred status of an email."""
    email = get_object_or_404(Email, pk=pk)
    email.is_starred = not email.is_starred
    email.save(update_fields=['is_starred'])
    # Go back to where the user came from
    return redirect(request.META.get('HTTP_REFERER', 'app:inbox'))


def delete_email(request, pk):
    """Move an email to trash, or delete permanently if already in trash."""
    email = get_object_or_404(Email, pk=pk)
    if email.folder == 'trash':
        email.delete()
        messages.info(request, 'Email deleted permanently.')
    else:
        email.folder = 'trash'
        email.save(update_fields=['folder'])
        messages.info(request, 'Email moved to trash.')
    return redirect(request.META.get('HTTP_REFERER', 'app:inbox'))


def empty_trash(request):
    """Permanently delete all emails in the trash."""
    if request.method == 'POST':
        deleted_count = Email.objects.filter(folder='trash').delete()[0]
        messages.success(request, f'Trash emptied. {deleted_count} messages deleted.')
    return redirect('app:inbox', folder='trash')