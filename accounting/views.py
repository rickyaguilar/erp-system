from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required
def overview_view(request):
    """Accounting Overview view"""
    context = {
        'page_title': 'Accounting Overview',
        'module': 'accounting'
    }
    return render(request, 'accounting/overview.html', context)


@never_cache
@login_required
def liquidation_form_view(request):
    """Liquidation Form view"""
    context = {
        'page_title': 'Liquidation Form',
        'module': 'accounting'
    }
    return render(request, 'accounting/liquidation_form.html', context)


@never_cache
@login_required
def debit_memo_view(request):
    """Debit Memo view"""
    context = {
        'page_title': 'Debit Memo',
        'module': 'accounting'
    }
    return render(request, 'accounting/debit_memo.html', context)


@never_cache
@login_required
def check_voucher_view(request):
    """Check Voucher view"""
    context = {
        'page_title': 'Check Voucher',
        'module': 'accounting'
    }
    return render(request, 'accounting/check_voucher.html', context)


@never_cache
@login_required
def disbursement_view(request):
    """Disbursement view"""
    context = {
        'page_title': 'Disbursement',
        'module': 'accounting'
    }
    return render(request, 'accounting/disbursement.html', context)
