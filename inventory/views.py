from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required
def purchase_view(request):
    """Purchase management view - shows only approved material requests"""
    from .models import MaterialRequest
    from django.core.paginator import Paginator
    
    # Get only approved requests
    approved_requests = MaterialRequest.objects.filter(status='approved').order_by('-created_at')
    
    # Add pagination
    paginator = Paginator(approved_requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Purchase Management',
        'module': 'inventory',
        'requests': page_obj,
        'total_requests': approved_requests.count(),
    }
    return render(request, 'inventory/purchase.html', context)


@never_cache
@login_required
def delivery_view(request):
    """Delivery management view"""
    context = {
        'page_title': 'Delivery Management',
        'module': 'inventory'
    }
    return render(request, 'inventory/delivery.html', context)


@never_cache
@login_required
def masterlist_view(request):
    """Masterlist view with pagination"""
    from django.core.paginator import Paginator
    from .models import InventoryItem
    
    items_list = InventoryItem.objects.all()
    paginator = Paginator(items_list, 10)  # Show 10 items per page
    
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Masterlist',
        'module': 'inventory',
        'items': items,
        'total_items': items_list.count()
    }
    return render(request, 'inventory/masterlist.html', context)


@never_cache
@login_required
def request_list_view(request):
    """Material Requests List view"""
    from .models import MaterialRequest
    from django.core.paginator import Paginator
    
    # Get all material requests ordered by most recent first
    requests = MaterialRequest.objects.select_related('requested_by').order_by('-created_at')
    
    # Add pagination
    paginator = Paginator(requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Request List',
        'module': 'inventory',
        'requests': page_obj,
        'total_requests': requests.count(),
    }
    return render(request, 'inventory/request_list.html', context)


@never_cache
@login_required
def request_form_view(request):
    """Material Request Form view"""
    from .forms import MaterialRequestForm, MaterialItemFormSet
    from .models import MaterialRequest
    from django.contrib import messages
    from django.shortcuts import redirect, get_object_or_404
    
    # Check if we're viewing/editing an existing request
    request_id = request.GET.get('id')
    existing_request = None
    is_approved = False
    if request_id:
        existing_request = get_object_or_404(MaterialRequest, id=request_id)
        is_approved = existing_request.status == 'approved'
    
    if request.method == 'POST':
        # Prevent editing approved requests
        if existing_request and is_approved:
            messages.error(request, 'Cannot edit an approved request.')
            return redirect('inventory:request_list')
        
        if existing_request:
            form = MaterialRequestForm(request.POST, instance=existing_request)
            formset = MaterialItemFormSet(request.POST, instance=existing_request)
        else:
            form = MaterialRequestForm(request.POST)
            formset = MaterialItemFormSet(request.POST)
        


        
        if form.is_valid() and formset.is_valid():
            # Save the main request
            material_request = form.save(commit=False)
            if not existing_request:
                material_request.requested_by = request.user
            material_request.save()
            
            # Save the material items
            formset.instance = material_request
            formset.save()
            
            action = "updated" if existing_request else "submitted"
            messages.success(request, f'Material request {material_request.request_number} has been {action} successfully!')
            return redirect('inventory:request_list')
        else:
            # Debug form errors
            if not form.is_valid():
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            
            if not formset.is_valid():
                for i, form_errors in enumerate(formset.errors):
                    if form_errors:
                        for field, errors in form_errors.items():
                            for error in errors:
                                messages.error(request, f'Material {i+1} - {field}: {error}')
                
                # Check non-form errors
                if formset.non_form_errors():
                    for error in formset.non_form_errors():
                        messages.error(request, f'Formset error: {error}')
            
            messages.error(request, 'Please correct the errors above.')
    else:
        if existing_request:
            form = MaterialRequestForm(instance=existing_request)
            formset = MaterialItemFormSet(instance=existing_request)
        else:
            form = MaterialRequestForm()
            formset = MaterialItemFormSet()
    
    context = {
        'page_title': 'Request Form',
        'module': 'inventory',
        'form': form,
        'formset': formset,
        'existing_request': existing_request,
        'is_approved': is_approved,
    }
    return render(request, 'inventory/request_form.html', context)


@never_cache
@login_required
def approve_request_view(request, request_id):
    """Approve a material request"""
    from .models import MaterialRequest
    from django.contrib import messages
    from django.shortcuts import redirect, get_object_or_404
    from django.utils import timezone
    
    if request.method == 'POST':
        material_request = get_object_or_404(MaterialRequest, id=request_id)
        
        # Only allow approval if status is pending
        if material_request.status == 'pending':
            material_request.status = 'approved'
            material_request.approved_by = request.user
            material_request.approved_date = timezone.now()
            material_request.save()
            
            messages.success(request, f'Material request {material_request.request_number} has been approved successfully!')
        else:
            messages.warning(request, f'Material request {material_request.request_number} cannot be approved (current status: {material_request.get_status_display()}).')
    
    return redirect('inventory:request_list')


@never_cache
@login_required
def request_details_api(request, request_id):
    """API endpoint to get request details in JSON format"""
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    from .models import MaterialRequest
    
    material_request = get_object_or_404(MaterialRequest, id=request_id)
    
    # Build items list
    items = []
    for item in material_request.items.all():
        items.append({
            'material_name': item.material_name,
            'quantity': float(item.quantity),
            'estimated_unit_price': float(item.estimated_unit_price),
        })
    
    # Build response data
    data = {
        'request_number': material_request.request_number,
        'requested_by': material_request.requested_by.get_full_name() or material_request.requested_by.username,
        'project_name': material_request.project_name,
        'site_supervisor': material_request.site_supervisor,
        'purpose': material_request.purpose,
        'created_at': material_request.created_at.strftime('%b %d, %Y'),
        'project_location': material_request.project_location,
        'delivery_date_needed': material_request.delivery_date_needed.strftime('%b %d, %Y'),
        'status': material_request.get_status_display(),
        'purchase_status': material_request.purchase_status,
        'purchase_status_display': material_request.get_purchase_status_display(),
        'rejection_reason': material_request.remarks if material_request.purchase_status == 'rejected' else None,
        'approved_by': material_request.approved_by.get_full_name() or material_request.approved_by.username if material_request.approved_by else None,
        'approved_date': material_request.approved_date.strftime('%b %d, %Y') if material_request.approved_date else None,
        'purchase_approved_by': material_request.purchase_approved_by.get_full_name() or material_request.purchase_approved_by.username if material_request.purchase_approved_by else None,
        'purchase_approved_date': material_request.purchase_approved_date.strftime('%b %d, %Y') if material_request.purchase_approved_date else None,
        'items': items,
    }
    
    return JsonResponse(data)


@never_cache
@login_required
def approve_purchase_view(request, request_id):
    """Approve a material request for purchase"""
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    from django.utils import timezone
    from .models import MaterialRequest
    
    if request.method == 'POST':
        material_request = get_object_or_404(MaterialRequest, id=request_id)
        
        # Update purchase status
        material_request.purchase_status = 'approved_for_purchase'
        material_request.purchase_approved_by = request.user
        material_request.purchase_approved_date = timezone.now()
        material_request.save()
        
        return JsonResponse({'success': True, 'message': f'Material request {material_request.request_number} has been approved successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@never_cache
@login_required
def reject_purchase_view(request, request_id):
    """Reject a material request for purchase"""
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    from django.utils import timezone
    from .models import MaterialRequest
    import json
    
    if request.method == 'POST':
        material_request = get_object_or_404(MaterialRequest, id=request_id)
        
        # Get rejection reason from POST data
        data = json.loads(request.body)
        reason = data.get('reason', '')
        
        # Update purchase status and remarks
        material_request.purchase_status = 'rejected'
        material_request.remarks = reason
        material_request.purchase_approved_by = request.user
        material_request.purchase_approved_date = timezone.now()
        material_request.save()
        
        return JsonResponse({'success': True, 'message': f'Material request {material_request.request_number} has been rejected successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

