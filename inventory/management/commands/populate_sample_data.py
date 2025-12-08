from django.core.management.base import BaseCommand
from inventory.models import InventoryItem

class Command(BaseCommand):
    help = 'Populates sample inventory data'

    def handle(self, *args, **options):
        # Create sample inventory items
        items_data = [
            {'item_code': 'MAT-001', 'material_name': 'Cement 50kg', 'category': 'Construction Materials', 'unit': 'bags', 'quantity_on_hand': 500, 'unit_price': 250.00},
            {'item_code': 'MAT-002', 'material_name': 'Steel Rebar 10mm', 'category': 'Construction Materials', 'unit': 'pcs', 'quantity_on_hand': 1000, 'unit_price': 150.00},
            {'item_code': 'MAT-003', 'material_name': 'Hollow Blocks', 'category': 'Construction Materials', 'unit': 'pcs', 'quantity_on_hand': 5000, 'unit_price': 12.50},
            {'item_code': 'MAT-004', 'material_name': 'Sand', 'category': 'Construction Materials', 'unit': 'cubic_meters', 'quantity_on_hand': 50, 'unit_price': 800.00},
            {'item_code': 'MAT-005', 'material_name': 'Gravel', 'category': 'Construction Materials', 'unit': 'cubic_meters', 'quantity_on_hand': 50, 'unit_price': 900.00},
            {'item_code': 'TOOL-001', 'material_name': 'Power Drill', 'category': 'Tools', 'unit': 'pcs', 'quantity_on_hand': 10, 'unit_price': 3500.00},
            {'item_code': 'TOOL-002', 'material_name': 'Hammer', 'category': 'Tools', 'unit': 'pcs', 'quantity_on_hand': 25, 'unit_price': 450.00},
            {'item_code': 'SAFE-001', 'material_name': 'Safety Helmet', 'category': 'Safety Equipment', 'unit': 'pcs', 'quantity_on_hand': 100, 'unit_price': 350.00},
            {'item_code': 'SAFE-002', 'material_name': 'Safety Vest', 'category': 'Safety Equipment', 'unit': 'pcs', 'quantity_on_hand': 100, 'unit_price': 200.00},
            {'item_code': 'ELEC-001', 'material_name': 'Electrical Wire 2.0mm', 'category': 'Electrical', 'unit': 'linear_meters', 'quantity_on_hand': 1000, 'unit_price': 25.00},
            {'item_code': 'PLUMB-001', 'material_name': 'PVC Pipe 1/2"', 'category': 'Plumbing', 'unit': 'linear_meters', 'quantity_on_hand': 500, 'unit_price': 45.00},
            {'item_code': 'MAT-006', 'material_name': 'Paint White 4L', 'category': 'Construction Materials', 'unit': 'liters', 'quantity_on_hand': 50, 'unit_price': 850.00},
            {'item_code': 'MAT-007', 'material_name': 'Plywood 1/2" x 4x8', 'category': 'Construction Materials', 'unit': 'pcs', 'quantity_on_hand': 75, 'unit_price': 620.00},
            {'item_code': 'TOOL-003', 'material_name': 'Circular Saw', 'category': 'Tools', 'unit': 'pcs', 'quantity_on_hand': 5, 'unit_price': 5500.00},
            {'item_code': 'SAFE-003', 'material_name': 'Safety Gloves', 'category': 'Safety Equipment', 'unit': 'pcs', 'quantity_on_hand': 150, 'unit_price': 120.00},
        ]
        
        for item_data in items_data:
            item, created = InventoryItem.objects.get_or_create(
                item_code=item_data['item_code'],
                defaults={
                    'material_name': item_data['material_name'],
                    'category': item_data['category'],
                    'unit': item_data['unit'],
                    'quantity_on_hand': item_data['quantity_on_hand'],
                    'unit_price': item_data['unit_price']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {item_data["item_code"]} - {item_data["material_name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {item_data["item_code"]}'))

        self.stdout.write(self.style.SUCCESS('\nSample inventory data population complete!'))

