from django.db import models

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Aperto'),
        ('in_progress', 'In lavorazione'),
        ('resolved', 'Risolto'),
        ('closed', 'Chiuso'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tickets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resort = models.ForeignKey('resort.Resort', on_delete=models.CASCADE, related_name='tickets')
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class TicketComment(models.Model):
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} @ {self.created_at}"

class TicketHistory(models.Model):
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='history')
    author = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)  # es. "Stato cambiato in...", "Nota aggiunta", ecc.
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
