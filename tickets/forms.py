from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Scrivi una risposta...'}),
        }

from accounts.models import User  # importa il modello utente personalizzato

class TicketAssignForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(role='maintainer'),
        required=False,
        label='Assegna a manutentore',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
