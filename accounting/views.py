from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.utils import timezone
from django.db import models
from .models import Liquidation, LiquidationItem, DebitMemo, CheckVoucher, Disbursement


@never_cache
@login_required
def overview_view(request):
    """Accounting Overview view"""
    
    # Get summary statistics
    pending_liquidations = Liquidation.objects.filter(status='submitted').count()
    pending_check_vouchers = CheckVoucher.objects.filter(status='pending').count()
    total_disbursements = Disbursement.objects.filter(status='completed').count()
    total_debit_memos = DebitMemo.objects.filter(status='posted').count()
    recent_disbursements = Disbursement.objects.filter(status='completed').order_by('-disbursement_date')[:5]
    
    # Current month
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    total_disbursed_this_month = Disbursement.objects.filter(
        disbursement_date__month=current_month,
        disbursement_date__year=current_year,
        status='completed'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    # Last month
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    total_disbursed_last_month = Disbursement.objects.filter(
        disbursement_date__month=last_month,
        disbursement_date__year=last_month_year,
        status='completed'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'page_title': 'Accounting Overview',
        'module': 'accounting',
        'pending_liquidations': pending_liquidations,
        'pending_check_vouchers': pending_check_vouchers,
        'total_disbursements': total_disbursements,
        'total_debit_memos': total_debit_memos,
        'recent_disbursements': recent_disbursements,
        'total_disbursed_this_month': total_disbursed_this_month,
        'total_disbursed_last_month': total_disbursed_last_month,
    }
    return render(request, 'accounting/overview.html', context)


@never_cache
@login_required
def liquidation_form_view(request):
    """Liquidation Form view"""
    if request.method == 'POST':
        # Create liquidation
        liquidation = Liquidation.objects.create(
            employee=request.user,
            project_name=request.POST.get('project_name'),
            cash_advance_amount=request.POST.get('cash_advance_amount'),
            cash_advance_date=request.POST.get('cash_advance_date'),
            liquidation_date=request.POST.get('liquidation_date'),
            status='submitted'
        )
        
        # Create liquidation items from form data
        item_dates = request.POST.getlist('item_date[]')
        item_descriptions = request.POST.getlist('item_description[]')
        item_categories = request.POST.getlist('item_category[]')
        item_amounts = request.POST.getlist('item_amount[]')
        item_receipts = request.POST.getlist('item_receipt[]')
        
        total_expenses = 0
        for i in range(len(item_dates)):
            if item_descriptions[i]:
                amount = float(item_amounts[i])
                total_expenses += amount
                LiquidationItem.objects.create(
                    liquidation=liquidation,
                    date=item_dates[i],
                    description=item_descriptions[i],
                    category=item_categories[i],
                    amount=amount,
                    receipt_number=item_receipts[i]
                )
        
        liquidation.total_expenses = total_expenses
        liquidation.save()
        
        messages.success(request, f'Liquidation {liquidation.liquidation_number} created successfully!')
        return redirect('accounting:overview')
    
    context = {
        'page_title': 'Liquidation Form',
        'module': 'accounting'
    }
    return render(request, 'accounting/liquidation_form.html', context)


@never_cache
@login_required
def debit_memo_view(request):
    """Debit Memo view"""
    if request.method == 'POST':
        memo = DebitMemo.objects.create(
            memo_date=request.POST.get('memo_date'),
            vendor_name=request.POST.get('vendor_name'),
            vendor_address=request.POST.get('vendor_address'),
            reference_invoice=request.POST.get('reference_invoice'),
            reason=request.POST.get('reason'),
            amount=request.POST.get('amount'),
            prepared_by=request.user,
            status='posted'
        )
        
        messages.success(request, f'Debit Memo {memo.memo_number} created successfully!')
        return redirect('accounting:overview')
    
    context = {
        'page_title': 'Debit Memo',
        'module': 'accounting'
    }
    return render(request, 'accounting/debit_memo.html', context)


@never_cache
@login_required
def check_voucher_view(request):
    """Check Voucher view"""
    if request.method == 'POST':
        voucher = CheckVoucher.objects.create(
            voucher_date=request.POST.get('voucher_date'),
            payee_name=request.POST.get('payee_name'),
            payee_address=request.POST.get('payee_address'),
            check_number=request.POST.get('check_number'),
            check_date=request.POST.get('check_date') or None,
            bank_name=request.POST.get('bank_name'),
            amount=request.POST.get('amount'),
            amount_in_words=request.POST.get('amount_in_words'),
            particulars=request.POST.get('particulars'),
            invoice_number=request.POST.get('invoice_number'),
            project_name=request.POST.get('project_name'),
            prepared_by=request.user,
            status='approved'
        )
        
        messages.success(request, f'Check Voucher {voucher.voucher_number} created successfully!')
        return redirect('accounting:overview')
    
    context = {
        'page_title': 'Check Voucher',
        'module': 'accounting'
    }
    return render(request, 'accounting/check_voucher.html', context)


@never_cache
@login_required
def disbursement_view(request):
    """Disbursement view"""
    if request.method == 'POST':
        disbursement = Disbursement.objects.create(
            disbursement_date=request.POST.get('disbursement_date'),
            recipient_name=request.POST.get('recipient_name'),
            recipient_type=request.POST.get('recipient_type'),
            amount=request.POST.get('amount'),
            payment_method=request.POST.get('payment_method'),
            reference_number=request.POST.get('reference_number'),
            purpose=request.POST.get('purpose'),
            category=request.POST.get('category'),
            project_name=request.POST.get('project_name'),
            processed_by=request.user,
            status='completed'
        )
        
        messages.success(request, f'Disbursement {disbursement.disbursement_number} recorded successfully!')
        return redirect('accounting:overview')
    
    context = {
        'page_title': 'Disbursement',
        'module': 'accounting'
    }
    return render(request, 'accounting/disbursement.html', context)
