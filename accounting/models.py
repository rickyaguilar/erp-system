from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Liquidation(models.Model):
    """Liquidation Report for cash advances and expenses"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    liquidation_number = models.CharField(max_length=50, unique=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liquidations')
    project_name = models.CharField(max_length=200)
    
    # Cash Advance Details
    cash_advance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_advance_date = models.DateField()
    
    # Liquidation Details
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    liquidation_date = models.DateField(default=timezone.now)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_liquidations')
    approved_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.liquidation_number} - {self.employee.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.liquidation_number:
            today = timezone.now().date()
            date_str = today.strftime('%Y%m%d')
            count = Liquidation.objects.filter(created_at__date=today).count() + 1
            self.liquidation_number = f"LIQ-{date_str}-{count:03d}"
        super().save(*args, **kwargs)
    
    @property
    def balance(self):
        return self.cash_advance_amount - self.total_expenses
    
    @property
    def refund_due(self):
        balance = self.balance
        return balance if balance > 0 else 0
    
    @property
    def reimbursement_due(self):
        balance = self.balance
        return abs(balance) if balance < 0 else 0


class LiquidationItem(models.Model):
    """Individual expense items in liquidation"""
    
    liquidation = models.ForeignKey(Liquidation, on_delete=models.CASCADE, related_name='items')
    date = models.DateField()
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.description} - ₱{self.amount}"


class DebitMemo(models.Model):
    """Debit Memo for adjustments and corrections"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ]
    
    memo_number = models.CharField(max_length=50, unique=True, blank=True)
    memo_date = models.DateField(default=timezone.now)
    
    # Vendor/Supplier Information
    vendor_name = models.CharField(max_length=200)
    vendor_address = models.TextField(blank=True)
    
    # Memo Details
    reference_invoice = models.CharField(max_length=100, blank=True)
    reason = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prepared_debit_memos')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_debit_memos')
    approved_date = models.DateTimeField(null=True, blank=True)
    
    remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.memo_number} - {self.vendor_name}"
    
    def save(self, *args, **kwargs):
        if not self.memo_number:
            today = timezone.now().date()
            date_str = today.strftime('%Y%m%d')
            count = DebitMemo.objects.filter(created_at__date=today).count() + 1
            self.memo_number = f"DM-{date_str}-{count:03d}"
        super().save(*args, **kwargs)


class CheckVoucher(models.Model):
    """Check Voucher for payments"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    voucher_number = models.CharField(max_length=50, unique=True, blank=True)
    voucher_date = models.DateField(default=timezone.now)
    
    # Payee Information
    payee_name = models.CharField(max_length=200)
    payee_address = models.TextField(blank=True)
    
    # Check Details
    check_number = models.CharField(max_length=50, blank=True)
    check_date = models.DateField(null=True, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    
    # Payment Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_in_words = models.CharField(max_length=500, blank=True)
    particulars = models.TextField()
    
    # References
    invoice_number = models.CharField(max_length=100, blank=True)
    project_name = models.CharField(max_length=200, blank=True)
    
    # Status and Approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prepared_check_vouchers')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_check_vouchers')
    approved_date = models.DateTimeField(null=True, blank=True)
    
    remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.voucher_number} - {self.payee_name}"
    
    def save(self, *args, **kwargs):
        if not self.voucher_number:
            today = timezone.now().date()
            date_str = today.strftime('%Y%m%d')
            count = CheckVoucher.objects.filter(created_at__date=today).count() + 1
            self.voucher_number = f"CV-{date_str}-{count:03d}"
        super().save(*args, **kwargs)


class Disbursement(models.Model):
    """Cash Disbursement Record"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    disbursement_number = models.CharField(max_length=50, unique=True, blank=True)
    disbursement_date = models.DateField(default=timezone.now)
    
    # Recipient Information
    recipient_name = models.CharField(max_length=200)
    recipient_type = models.CharField(max_length=100)  # Supplier, Employee, Contractor, etc.
    
    # Payment Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference_number = models.CharField(max_length=100, blank=True)  # Check number, transaction ID, etc.
    
    # Purpose
    purpose = models.TextField()
    category = models.CharField(max_length=100)  # Operating Expense, Project Cost, Payroll, etc.
    project_name = models.CharField(max_length=200, blank=True)
    
    # References
    check_voucher = models.ForeignKey(CheckVoucher, on_delete=models.SET_NULL, null=True, blank=True, related_name='disbursements')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_disbursements')
    
    remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-disbursement_date']
    
    def __str__(self):
        return f"{self.disbursement_number} - {self.recipient_name}"
    
    def save(self, *args, **kwargs):
        if not self.disbursement_number:
            today = timezone.now().date()
            date_str = today.strftime('%Y%m%d')
            count = Disbursement.objects.filter(created_at__date=today).count() + 1
            self.disbursement_number = f"DISB-{date_str}-{count:03d}"
        super().save(*args, **kwargs)
