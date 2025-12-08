from django import template
from django.utils import timezone
from inventory.models import MaterialRequest

register = template.Library()

@register.simple_tag
def get_next_request_number():
    """Generate the next request number for new requests"""
    today = timezone.now().date()
    date_str = today.strftime('%Y%m%d')
    
    # Count existing requests for today
    count = MaterialRequest.objects.filter(created_at__date=today).count() + 1
    
    return f"REQ-{date_str}-{count:03d}"