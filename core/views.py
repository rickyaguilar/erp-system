from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


class CustomLoginView(LoginView):
    """Custom login view with additional context"""
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, redirect to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self):
        form = super().get_form()
        form.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter Username'
        })
        form.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter Password'
        })
        return form

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


@never_cache
@login_required
def dashboard_view(request):
    """Dashboard view - main landing page after login"""
    # Get some basic statistics for the dashboard
    total_users = User.objects.count()
    active_sessions = 1  # Simplified for now - could be enhanced to count actual active sessions
    
    # Sample construction projects data
    projects = [
        {
            'id': 1,
            'name': 'Metro Tower Construction',
            'location': 'Makati City',
            'status': 'In Progress',
            'progress': 65,
            'budget': 45000000,
            'spent': 29250000,
            'receivables': 15750000,
            'payables': 8500000,
            'start_date': '2024-03-15',
            'target_completion': '2025-09-30',
            'budget_status': 'on_budget',  # spent < 90% of budget
        },
        {
            'id': 2,
            'name': 'Highway Expansion Project',
            'location': 'Quezon City',
            'status': 'In Progress',
            'progress': 42,
            'budget': 78000000,
            'spent': 32760000,
            'receivables': 45240000,
            'payables': 12300000,
            'start_date': '2024-06-01',
            'target_completion': '2026-02-28',
            'budget_status': 'on_budget',
        },
        {
            'id': 3,
            'name': 'Residential Complex Phase 2',
            'location': 'Taguig City',
            'status': 'In Progress',
            'progress': 78,
            'budget': 62000000,
            'spent': 48360000,
            'receivables': 13640000,
            'payables': 5800000,
            'start_date': '2023-11-10',
            'target_completion': '2025-05-15',
            'budget_status': 'on_budget',
        },
        {
            'id': 4,
            'name': 'Bridge Rehabilitation',
            'location': 'Pasig City',
            'status': 'Planning',
            'progress': 15,
            'budget': 35000000,
            'spent': 5250000,
            'receivables': 29750000,
            'payables': 2100000,
            'start_date': '2024-11-01',
            'target_completion': '2025-12-31',
            'budget_status': 'on_budget',
        },
        {
            'id': 5,
            'name': 'Commercial Plaza Development',
            'location': 'Mandaluyong City',
            'status': 'Completed',
            'progress': 100,
            'budget': 52000000,
            'spent': 51200000,
            'receivables': 0,
            'payables': 800000,
            'start_date': '2023-02-20',
            'target_completion': '2024-10-31',
            'budget_status': 'near_budget',  # spent >= 90% of budget
        },
    ]
    
    # Calculate budget status for each project
    for project in projects:
        if project['spent'] > project['budget']:
            project['budget_status'] = 'over_budget'
        elif project['spent'] >= project['budget'] * 0.9:
            project['budget_status'] = 'near_budget'
        else:
            project['budget_status'] = 'on_budget'
    
    # Calculate totals for financial summary
    total_budget = sum(p['budget'] for p in projects)
    total_spent = sum(p['spent'] for p in projects)
    total_receivables = sum(p['receivables'] for p in projects)
    total_payables = sum(p['payables'] for p in projects)
    
    # Count projects by status
    in_progress = len([p for p in projects if p['status'] == 'In Progress'])
    planning = len([p for p in projects if p['status'] == 'Planning'])
    completed = len([p for p in projects if p['status'] == 'Completed'])
    
    context = {
        'total_users': total_users,
        'active_sessions': active_sessions,
        'user': request.user,
        'projects': projects,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_receivables': total_receivables,
        'total_payables': total_payables,
        'in_progress': in_progress,
        'planning': planning,
        'completed': completed,
        'total_projects': len(projects),
    }
    
    response = render(request, 'dashboard.html', context)
    
    # Add cache control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response
