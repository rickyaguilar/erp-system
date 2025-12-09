"""
Populate accounting data for Render deployment
This script checks if data already exists before populating
"""
import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from django.contrib.auth.models import User
from accounting.models import Liquidation, LiquidationItem, DebitMemo, CheckVoucher, Disbursement

# Check if data already exists
if Liquidation.objects.exists() or DebitMemo.objects.exists() or CheckVoucher.objects.exists() or Disbursement.objects.exists():
    print("Accounting data already exists. Skipping population.")
    print(f"  - Liquidations: {Liquidation.objects.count()}")
    print(f"  - Debit Memos: {DebitMemo.objects.count()}")
    print(f"  - Check Vouchers: {CheckVoucher.objects.count()}")
    print(f"  - Disbursements: {Disbursement.objects.count()}")
    exit(0)

# Get or create a user for the records
user = User.objects.filter(is_superuser=True).first()
if not user:
    print("No superuser found. Creating default superuser...")
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='System',
        last_name='Administrator'
    )
    print(f"Created superuser: {user.username}")

print(f"Using user: {user.username}")

# Helper function to get dates
def get_date(days_ago):
    return datetime.now().date() - timedelta(days=days_ago)

# Create Liquidations
print("\nCreating Liquidations...")
liquidations_data = [
    {
        'project_name': 'Makati Office Building Phase 2',
        'cash_advance_amount': Decimal('50000.00'),
        'cash_advance_date': get_date(15),
        'liquidation_date': get_date(5),
        'status': 'submitted',
        'items': [
            {'date': get_date(14), 'description': 'Transportation to site', 'category': 'Transportation', 'amount': Decimal('2500.00'), 'receipt_no': 'TR-001'},
            {'date': get_date(13), 'description': 'Cement and gravel', 'category': 'Materials', 'amount': Decimal('28000.00'), 'receipt_no': 'MT-042'},
            {'date': get_date(12), 'description': 'Labor payment', 'category': 'Labor', 'amount': Decimal('15000.00'), 'receipt_no': 'LB-089'},
            {'date': get_date(10), 'description': 'Meals for workers', 'category': 'Meals', 'amount': Decimal('3200.00'), 'receipt_no': 'ML-023'},
        ]
    },
    {
        'project_name': 'Quezon City Residential Complex',
        'cash_advance_amount': Decimal('75000.00'),
        'cash_advance_date': get_date(20),
        'liquidation_date': get_date(8),
        'status': 'approved',
        'items': [
            {'date': get_date(19), 'description': 'Steel rebar delivery', 'category': 'Materials', 'amount': Decimal('45000.00'), 'receipt_no': 'MT-055'},
            {'date': get_date(18), 'description': 'Electrical wiring', 'category': 'Materials', 'amount': Decimal('18500.00'), 'receipt_no': 'MT-056'},
            {'date': get_date(17), 'description': 'Site transportation', 'category': 'Transportation', 'amount': Decimal('3500.00'), 'receipt_no': 'TR-012'},
            {'date': get_date(15), 'description': 'Utility bills', 'category': 'Utilities', 'amount': Decimal('5200.00'), 'receipt_no': 'UT-008'},
        ]
    },
    {
        'project_name': 'BGC Commercial Tower',
        'cash_advance_amount': Decimal('100000.00'),
        'cash_advance_date': get_date(25),
        'liquidation_date': get_date(12),
        'status': 'submitted',
        'items': [
            {'date': get_date(24), 'description': 'Plywood and lumber', 'category': 'Materials', 'amount': Decimal('32000.00'), 'receipt_no': 'MT-061'},
            {'date': get_date(23), 'description': 'Paint and coatings', 'category': 'Materials', 'amount': Decimal('28500.00'), 'receipt_no': 'MT-062'},
            {'date': get_date(22), 'description': 'Labor - carpenters', 'category': 'Labor', 'amount': Decimal('25000.00'), 'receipt_no': 'LB-095'},
            {'date': get_date(20), 'description': 'Equipment rental', 'category': 'Others', 'amount': Decimal('12000.00'), 'receipt_no': 'EQ-018'},
        ]
    },
    {
        'project_name': 'Pasig Warehouse Construction',
        'cash_advance_amount': Decimal('60000.00'),
        'cash_advance_date': get_date(10),
        'liquidation_date': get_date(3),
        'status': 'draft',
        'items': [
            {'date': get_date(9), 'description': 'Roofing materials', 'category': 'Materials', 'amount': Decimal('35000.00'), 'receipt_no': 'MT-068'},
            {'date': get_date(8), 'description': 'Transportation', 'category': 'Transportation', 'amount': Decimal('4500.00'), 'receipt_no': 'TR-020'},
            {'date': get_date(7), 'description': 'Worker meals', 'category': 'Meals', 'amount': Decimal('2800.00'), 'receipt_no': 'ML-035'},
        ]
    },
]

for liq_data in liquidations_data:
    items = liq_data.pop('items')
    liquidation = Liquidation.objects.create(
        employee=user,
        **liq_data
    )
    
    for item_data in items:
        LiquidationItem.objects.create(
            liquidation=liquidation,
            date=item_data['date'],
            description=item_data['description'],
            category=item_data['category'],
            amount=item_data['amount'],
            receipt_number=item_data['receipt_no']
        )
    
    # Update total_expenses
    liquidation.total_expenses = sum(item.amount for item in liquidation.items.all())
    liquidation.save()
    
    print(f"Created Liquidation: {liquidation.liquidation_number} - {liquidation.project_name}")

# Create Debit Memos
print("\nCreating Debit Memos...")
debit_memos_data = [
    {
        'vendor_name': 'ABC Construction Supplies Inc.',
        'reference_invoice': 'INV-2024-1234',
        'memo_date': get_date(30),
        'amount': Decimal('14250.00'),
        'reason': 'Damaged cement bags - 50 bags short delivered',
        'status': 'posted',
    },
    {
        'vendor_name': 'Steel World Corporation',
        'reference_invoice': 'INV-2024-5678',
        'memo_date': get_date(25),
        'amount': Decimal('28500.00'),
        'reason': 'Incorrect specifications - 10mm rebar instead of 12mm',
        'status': 'posted',
    },
    {
        'vendor_name': 'Premium Paints & Coatings',
        'reference_invoice': 'INV-2024-9012',
        'memo_date': get_date(20),
        'amount': Decimal('13500.00'),
        'reason': 'Wrong color shade delivered',
        'status': 'draft',
    },
    {
        'vendor_name': 'Metro Plumbing Supplies',
        'reference_invoice': 'INV-2024-3456',
        'memo_date': get_date(15),
        'amount': Decimal('8400.00'),
        'reason': 'Defective PVC pipes - leaking',
        'status': 'posted',
    },
]

for dm_data in debit_memos_data:
    debit_memo = DebitMemo.objects.create(
        prepared_by=user,
        **dm_data
    )
    print(f"Created Debit Memo: {debit_memo.memo_number} - {debit_memo.vendor_name}")

# Create Check Vouchers
print("\nCreating Check Vouchers...")
check_vouchers_data = [
    {
        'payee_name': 'ABC Construction Supplies Inc.',
        'amount': Decimal('245000.00'),
        'particulars': 'Payment for cement and aggregates delivery',
        'check_date': get_date(5),
        'check_number': 'CHK-001236',
        'status': 'approved',
    },
    {
        'payee_name': 'Metro Electrical Supplies',
        'amount': Decimal('156000.00'),
        'particulars': 'Payment for electrical materials - November billing',
        'check_date': get_date(8),
        'check_number': 'CHK-001241',
        'status': 'pending',
    },
    {
        'payee_name': 'Steel World Corporation',
        'amount': Decimal('385000.00'),
        'particulars': 'Payment for steel rebar and structural materials',
        'check_date': get_date(10),
        'check_number': 'CHK-001237',
        'status': 'approved',
    },
    {
        'payee_name': 'Global Hardware Trading',
        'amount': Decimal('98000.00'),
        'particulars': 'Payment for tools and hardware supplies',
        'check_date': get_date(12),
        'check_number': 'CHK-001242',
        'status': 'pending',
    },
    {
        'payee_name': 'Premium Paints & Coatings',
        'amount': Decimal('127000.00'),
        'particulars': 'Payment for paint and finishing materials',
        'check_date': get_date(15),
        'check_number': 'CHK-001238',
        'status': 'approved',
    },
]

for cv_data in check_vouchers_data:
    check_voucher = CheckVoucher.objects.create(
        prepared_by=user,
        **cv_data
    )
    if cv_data['status'] == 'approved':
        check_voucher.approved_by = user
        check_voucher.save()
    print(f"Created Check Voucher: {check_voucher.voucher_number} - {check_voucher.payee_name}")

# Create Disbursements
print("\nCreating Disbursements...")
disbursements_data = [
    {
        'recipient_name': 'Juan dela Cruz',
        'recipient_type': 'Employee',
        'amount': Decimal('25000.00'),
        'purpose': 'Salary - Site Supervisor',
        'category': 'Payroll',
        'disbursement_date': get_date(30),
        'payment_method': 'check',
        'reference_number': 'CHK-001234',
        'status': 'completed',
    },
    {
        'recipient_name': 'Maria Santos',
        'recipient_type': 'Employee',
        'amount': Decimal('22000.00'),
        'purpose': 'Salary - Project Engineer',
        'category': 'Payroll',
        'disbursement_date': get_date(30),
        'payment_method': 'check',
        'reference_number': 'CHK-001235',
        'status': 'completed',
    },
    {
        'recipient_name': 'ABC Construction Supplies Inc.',
        'recipient_type': 'Supplier',
        'amount': Decimal('245000.00'),
        'purpose': 'Payment for cement and aggregates delivery',
        'category': 'Project Cost',
        'disbursement_date': get_date(25),
        'payment_method': 'check',
        'reference_number': 'CHK-001236',
        'status': 'completed',
    },
    {
        'recipient_name': 'Steel World Corporation',
        'recipient_type': 'Supplier',
        'amount': Decimal('385000.00'),
        'purpose': 'Payment for steel rebar and structural materials',
        'category': 'Project Cost',
        'disbursement_date': get_date(20),
        'payment_method': 'check',
        'reference_number': 'CHK-001237',
        'status': 'completed',
    },
    {
        'recipient_name': 'Metro Electrical Supplies',
        'recipient_type': 'Supplier',
        'amount': Decimal('156000.00'),
        'purpose': 'Payment for electrical materials',
        'category': 'Project Cost',
        'disbursement_date': get_date(18),
        'payment_method': 'bank_transfer',
        'reference_number': 'BT-20241115-0098',
        'status': 'completed',
    },
    {
        'recipient_name': 'Premium Paints & Coatings',
        'recipient_type': 'Supplier',
        'amount': Decimal('127000.00'),
        'purpose': 'Payment for paint and finishing materials',
        'category': 'Project Cost',
        'disbursement_date': get_date(15),
        'payment_method': 'check',
        'reference_number': 'CHK-001238',
        'status': 'completed',
    },
    {
        'recipient_name': 'Global Hardware Trading',
        'recipient_type': 'Supplier',
        'amount': Decimal('98000.00'),
        'purpose': 'Payment for tools and hardware supplies',
        'category': 'Operating Expense',
        'disbursement_date': get_date(12),
        'payment_method': 'check',
        'reference_number': 'CHK-001239',
        'status': 'completed',
    },
    {
        'recipient_name': 'Metro Plumbing Supplies',
        'recipient_type': 'Supplier',
        'amount': Decimal('85000.00'),
        'purpose': 'Payment for plumbing materials',
        'category': 'Project Cost',
        'disbursement_date': get_date(10),
        'payment_method': 'bank_transfer',
        'reference_number': 'BT-20241125-0124',
        'status': 'completed',
    },
    {
        'recipient_name': 'Quick Transport Services',
        'recipient_type': 'Contractor',
        'amount': Decimal('45000.00'),
        'purpose': 'Payment for material delivery services',
        'category': 'Operating Expense',
        'disbursement_date': get_date(8),
        'payment_method': 'cash',
        'reference_number': '',
        'status': 'completed',
    },
    {
        'recipient_name': 'City Power & Light',
        'recipient_type': 'Utility',
        'amount': Decimal('28500.00'),
        'purpose': 'Electricity bills - November',
        'category': 'Operating Expense',
        'disbursement_date': get_date(5),
        'payment_method': 'bank_transfer',
        'reference_number': 'BT-20241201-0156',
        'status': 'completed',
    },
    {
        'recipient_name': 'Office Supplies Express',
        'recipient_type': 'Supplier',
        'amount': Decimal('15000.00'),
        'purpose': 'Office supplies and equipment',
        'category': 'Operating Expense',
        'disbursement_date': get_date(3),
        'payment_method': 'check',
        'reference_number': 'CHK-001240',
        'status': 'completed',
    },
    {
        'recipient_name': 'Tech Solutions Inc.',
        'recipient_type': 'Supplier',
        'amount': Decimal('65000.00'),
        'purpose': 'Software licenses and IT support',
        'category': 'Operating Expense',
        'disbursement_date': get_date(2),
        'payment_method': 'bank_transfer',
        'reference_number': 'BT-20241205-0178',
        'status': 'completed',
    },
]

for disb_data in disbursements_data:
    disbursement = Disbursement.objects.create(
        processed_by=user,
        **disb_data
    )
    print(f"Created Disbursement: {disbursement.disbursement_number} - {disbursement.recipient_name}")

# Print summary
print("\n" + "="*60)
print("ACCOUNTING DATA POPULATION SUMMARY")
print("="*60)
print(f"Liquidations created: {Liquidation.objects.count()}")
print(f"  - Draft: {Liquidation.objects.filter(status='draft').count()}")
print(f"  - Submitted: {Liquidation.objects.filter(status='submitted').count()}")
print(f"  - Approved: {Liquidation.objects.filter(status='approved').count()}")
print(f"\nDebit Memos created: {DebitMemo.objects.count()}")
print(f"  - Draft: {DebitMemo.objects.filter(status='draft').count()}")
print(f"  - Posted: {DebitMemo.objects.filter(status='posted').count()}")
print(f"\nCheck Vouchers created: {CheckVoucher.objects.count()}")
print(f"  - Pending: {CheckVoucher.objects.filter(status='pending').count()}")
print(f"  - Approved: {CheckVoucher.objects.filter(status='approved').count()}")
print(f"\nDisbursements created: {Disbursement.objects.count()}")
print(f"  - Completed: {Disbursement.objects.filter(status='completed').count()}")
print("\n" + "="*60)

# Calculate totals
total_liquidation_amount = sum(liq.cash_advance_amount for liq in Liquidation.objects.all())
total_debit_amount = sum(dm.amount for dm in DebitMemo.objects.all())
total_check_amount = sum(cv.amount for cv in CheckVoucher.objects.all())
total_disbursement_amount = sum(disb.amount for disb in Disbursement.objects.all())

print(f"\nTotal Liquidation Amount: ₱{total_liquidation_amount:,.2f}")
print(f"Total Debit Memo Amount: ₱{total_debit_amount:,.2f}")
print(f"Total Check Voucher Amount: ₱{total_check_amount:,.2f}")
print(f"Total Disbursement Amount: ₱{total_disbursement_amount:,.2f}")
print("="*60)
print("\nAccounting data population completed successfully!")
