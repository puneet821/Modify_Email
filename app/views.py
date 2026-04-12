from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Email, Attachment
from .forms import ComposeEmailForm


def inbox(request):
    """Display all emails in the inbox, newest (by received_date) first."""
    query = request.GET.get('q', '')
    emails = Email.objects.all()

    if query:
        emails = emails.filter(subject__icontains=query) | emails.filter(
            body__icontains=query
        ) | emails.filter(sender__icontains=query)

    context = {
        'emails': emails,
        'query': query,
        'total_count': Email.objects.count(),
        'unread_count': Email.objects.filter(is_read=False).count(),
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

            messages.success(request, f'Email "{email.subject}" delivered to inbox!')
            return redirect('app:inbox')
    else:
        form = ComposeEmailForm()

    context = {
        'form': form,
        'unread_count': Email.objects.filter(is_read=False).count(),
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
        'unread_count': Email.objects.filter(is_read=False).count(),
    })


def toggle_star(request, pk):
    """Toggle the starred status of an email."""
    email = get_object_or_404(Email, pk=pk)
    email.is_starred = not email.is_starred
    email.save(update_fields=['is_starred'])
    # Go back to where the user came from
    return redirect(request.META.get('HTTP_REFERER', 'app:inbox'))


def delete_email(request, pk):
    """Delete an email."""
    email = get_object_or_404(Email, pk=pk)
    email.delete()
    messages.info(request, 'Email moved to trash.')
    return redirect('app:inbox')