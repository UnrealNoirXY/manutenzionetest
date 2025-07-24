from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from resort.models import Resort
from tickets.models import Ticket
from accounts.models import User

def home(request):
    if request.user.is_authenticated:
        role = getattr(request.user, "role", None)
        if role == 'superadmin':
            return redirect('dashboard_superadmin')
        elif role == 'receptionist':
            return redirect('dashboard_receptionist')
        elif role == 'maintainer':
            return redirect('dashboard_maintainer')
        else:
            return render(request, 'core/login.html', {'error': 'Utente senza ruolo. Contattare l\'amministratore.'})
    return render(request, 'core/login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {'error': 'Credenziali non valide'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_superadmin(request):
    if request.user.role != 'superadmin':
        return redirect('home')
    resort_count = Resort.objects.count()
    users_count = User.objects.count()
    tickets_open = Ticket.objects.filter(status='open').count()
    return render(request, 'core/dashboard_superadmin.html', {
        'resort_count': resort_count,
        'users_count': users_count,
        'tickets_open': tickets_open,
    })

@login_required
def dashboard_receptionist(request):
    if request.user.role != 'receptionist':
        return redirect('home')
    tickets = Ticket.objects.filter(resort=request.user.resort).order_by('-created_at')
    return render(request, 'core/dashboard_receptionist.html', {
        'tickets': tickets
    })

@login_required
def dashboard_maintainer(request):
    if request.user.role != 'maintainer':
        return redirect('home')
    tickets = Ticket.objects.filter(assigned_to=request.user).order_by('-created_at')
    return render(request, 'core/dashboard_maintainer.html', {
        'tickets': tickets
    })

