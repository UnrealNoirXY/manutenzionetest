from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, TicketComment, TicketHistory
from .forms import TicketAssignForm, TicketUpdateForm, TicketCommentForm
from accounts.models import User

@login_required
def ticket_create(request):
    # Reception e superadmin possono aprire ticket
    if request.user.role not in ['receptionist', 'superadmin']:
        return redirect('home')

    if request.method == 'POST':
        form = TicketAssignForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.resort = request.user.resort
            ticket.created_by = request.user
            ticket.save()
            form.save_m2m()
            return redirect('dashboard_receptionist')
    else:
        form = TicketAssignForm()
        # Reception vede solo i manutentori del proprio resort
        form.fields['assigned_to'].queryset = User.objects.filter(role='maintainer', resort=request.user.resort)

    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Permessi: manutentore assegnato, reception del resort, o superadmin
    if request.user.role == 'maintainer' and ticket.assigned_to != request.user:
        return redirect('dashboard_maintainer')
    if request.user.role == 'receptionist' and ticket.resort != request.user.resort:
        return redirect('dashboard_receptionist')

    can_edit = request.user.role in ['receptionist', 'maintainer', 'superadmin']
    # Reception e manutentore possono commentare e aggiornare stato
    if request.method == 'POST' and can_edit:
        update_form = TicketUpdateForm(request.POST, instance=ticket)
        comment_form = TicketCommentForm(request.POST)
        stato_vecchio = ticket.status
        history_log = []

        if update_form.is_valid():
            # Log della variazione di stato
            if update_form.cleaned_data['status'] != stato_vecchio:
                TicketHistory.objects.create(
                    ticket=ticket,
                    author=request.user,
                    action=f"Stato cambiato da {ticket.get_status_display()} a {dict(Ticket.STATUS_CHOICES)[update_form.cleaned_data['status']]}"
                )
            update_form.save()
        if comment_form.is_valid() and comment_form.cleaned_data['comment']:
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            TicketHistory.objects.create(
                ticket=ticket,
                author=request.user,
                action="Nota aggiunta"
            )
        return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        update_form = TicketUpdateForm(instance=ticket)
        comment_form = TicketCommentForm()

    comments = ticket.comments.all()
    history = ticket.history.all()

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'can_edit': can_edit,
        'update_form': update_form,
        'comment_form': comment_form,
        'comments': comments,
        'history': history,
    })
