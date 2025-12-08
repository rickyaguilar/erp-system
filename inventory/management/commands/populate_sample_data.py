from django.core.management.base import BaseCommand
from inventory.models import Category, Warehouse, Material

class Command(BaseCommand):
    help = 'Populates sample inventory data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            'Construction Materials',
            'Tools',
            'Safety Equipment',
            'Electrical',
            'Plumbing',
        ]
        
        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))

        # Create warehouses
        warehouses_data = [
            {'name': 'Main Warehouse', 'location': 'Central District'},
            {'name': 'Site Warehouse A', 'location': 'Project Site A'},
            {'name': 'Site Warehouse B', 'location': 'Project Site B'},
        ]
        
        warehouses = {}
        for wh_data in warehouses_data:
            wh, created = Warehouse.objects.get_or_create(
                name=wh_data['name'],
                defaults={'location': wh_data['location']}
            )
            warehouses[wh_data['name']] = wh
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created warehouse: {wh_data["name"]}'))

        # Create materials
        materials_data = [
            {'name': 'Cement 50kg', 'category': 'Construction Materials', 'unit': 'bags', 'quantity': 500, 'unit_price': 250.00},
            {'name': 'Steel Rebar 10mm', 'category': 'Construction Materials', 'unit': 'pcs', 'quantity': 1000, 'unit_price': 150.00},
            {'name': 'Hollow Blocks', 'category': 'Construction Materials', 'unit': 'pcs', 'quantity': 5000, 'unit_price': 12.50},
            {'name': 'Sand', 'category': 'Construction Materials', 'unit': 'cu.m', 'quantity': 50, 'unit_price': 800.00},
            {'name': 'Gravel', 'category': 'Construction Materials', 'unit': 'cu.m', 'quantity': 50, 'unit_price': 900.00},
            {'name': 'Power Drill', 'category': 'Tools', 'unit': 'pcs', 'quantity': 10, 'unit_price': 3500.00},
            {'name': 'Hammer', 'category': 'Tools', 'unit': 'pcs', 'quantity': 25, 'unit_price': 450.00},
            {'name': 'Safety Helmet', 'category': 'Safety Equipment', 'unit': 'pcs', 'quantity': 100, 'unit_price': 350.00},
            {'name': 'Safety Vest', 'category': 'Safety Equipment', 'unit': 'pcs', 'quantity': 100, 'unit_price': 200.00},
            {'name': 'Electrical Wire 2.0mm', 'category': 'Electrical', 'unit': 'meters', 'quantity': 1000, 'unit_price': 25.00},
            {'name': 'PVC Pipe 1/2"', 'category': 'Plumbing', 'unit': 'meters', 'quantity': 500, 'unit_price': 45.00},
        ]
        
        for mat_data in materials_data:
            cat = categories[mat_data['category']]
            mat, created = Material.objects.get_or_create(
                name=mat_data['name'],
                defaults={
                    'category': cat,
                    'unit': mat_data['unit'],
                    'quantity': mat_data['quantity'],
                    'unit_price': mat_data['unit_price']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created material: {mat_data["name"]}'))

        self.stdout.write(self.style.SUCCESS('Sample data population complete!'))
