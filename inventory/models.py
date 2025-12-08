from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MaterialRequest(models.Model):
    """Material Purchase Request for construction projects"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('ordered', 'Ordered'),
    ]
    
    PURCHASE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved_for_purchase', 'Approved for Purchase'),
        ('rejected', 'Rejected'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Request Information
    request_number = models.CharField(max_length=50, unique=True, blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_requests')
    request_date = models.DateTimeField(default=timezone.now)
    
    # Project Information
    project_name = models.CharField(max_length=200)
    project_location = models.TextField()
    site_supervisor = models.CharField(max_length=100)
    
    # Request Details
    purpose = models.TextField(help_text="Purpose of the material request")
    delivery_date_needed = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Status and Approval
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    purchase_status = models.CharField(max_length=25, choices=PURCHASE_STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    approved_date = models.DateTimeField(null=True, blank=True)
    purchase_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_approvals')
    purchase_approved_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Request {self.request_number} - {self.project_name}"
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            # Generate request number: REQ-YYYYMMDD-XXX
            today = timezone.now().date()
            date_str = today.strftime('%Y%m%d')
            count = MaterialRequest.objects.filter(created_at__date=today).count() + 1
            self.request_number = f"REQ-{date_str}-{count:03d}"
        super().save(*args, **kwargs)
    
    @property
    def total_estimated_cost(self):
        return sum(item.total_cost for item in self.items.all())
    
    @property
    def total_items_count(self):
        return self.items.count()


class MaterialRequestItem(models.Model):
    """Individual material items in a request"""
    
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('bags', 'Bags'),
        ('cubic_meters', 'Cubic Meters'),
        ('square_meters', 'Square Meters'),
        ('linear_meters', 'Linear Meters'),
        ('tons', 'Tons'),
        ('liters', 'Liters'),
        ('sets', 'Sets'),
        ('boxes', 'Boxes'),
        ('rolls', 'Rolls'),
    ]
    
    request = models.ForeignKey(MaterialRequest, on_delete=models.CASCADE, related_name='items')
    
    # Material Details
    material_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    specification = models.CharField(max_length=300, blank=True, help_text="Size, grade, brand, etc.")
    
    # Quantity and Pricing
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    estimated_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Additional Information
    supplier_preference = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.material_name} - {self.quantity} {self.unit}"
    
    @property
    def total_cost(self):
        return self.quantity * self.estimated_unit_price


class InventoryItem(models.Model):
    """Inventory Master List - tracks all materials in stock"""
    
    item_code = models.CharField(max_length=50, unique=True)
    material_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    quantity_on_hand = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['item_code']
    
    def __str__(self):
        return f"{self.item_code} - {self.material_name}"
    
    @property
    def total_value(self):
        return self.quantity_on_hand * self.unit_price
