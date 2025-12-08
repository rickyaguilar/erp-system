import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from inventory.models import InventoryItem

# Sample inventory data
inventory_data = [
    {"item_code": "MAT-001", "material_name": "Portland Cement", "category": "Construction Materials", "unit": "Bag (50kg)", "quantity_on_hand": 450, "unit_price": 285.00},
    {"item_code": "MAT-002", "material_name": "Steel Rebar 10mm", "category": "Steel & Metals", "unit": "Piece", "quantity_on_hand": 1200, "unit_price": 165.00},
    {"item_code": "MAT-003", "material_name": "Gravel (3/4\")", "category": "Aggregates", "unit": "Cubic Meter", "quantity_on_hand": 85, "unit_price": 1250.00},
    {"item_code": "MAT-004", "material_name": "Sand (Washed)", "category": "Aggregates", "unit": "Cubic Meter", "quantity_on_hand": 120, "unit_price": 950.00},
    {"item_code": "MAT-005", "material_name": "Hollow Blocks 4\"", "category": "Masonry", "unit": "Piece", "quantity_on_hand": 3500, "unit_price": 12.50},
    {"item_code": "MAT-006", "material_name": "Plywood 1/4\" x 4' x 8'", "category": "Wood & Lumber", "unit": "Sheet", "quantity_on_hand": 75, "unit_price": 485.00},
    {"item_code": "MAT-007", "material_name": "Paint (White) Interior", "category": "Paints & Coatings", "unit": "Gallon", "quantity_on_hand": 180, "unit_price": 1350.00},
    {"item_code": "MAT-008", "material_name": "GI Pipe 1\" x 20'", "category": "Plumbing", "unit": "Length", "quantity_on_hand": 250, "unit_price": 425.00},
    {"item_code": "MAT-009", "material_name": "Electrical Wire #12 THHN", "category": "Electrical", "unit": "Meter", "quantity_on_hand": 5000, "unit_price": 18.50},
    {"item_code": "MAT-010", "material_name": "Ceramic Tiles 60x60cm", "category": "Finishing Materials", "unit": "Box", "quantity_on_hand": 95, "unit_price": 875.00},
    {"item_code": "MAT-011", "material_name": "Roofing Sheets GI", "category": "Roofing Materials", "unit": "Sheet", "quantity_on_hand": 200, "unit_price": 650.00},
    {"item_code": "MAT-012", "material_name": "PVC Pipe 4\"", "category": "Plumbing", "unit": "Length", "quantity_on_hand": 150, "unit_price": 280.00},
    {"item_code": "MAT-013", "material_name": "Nails Assorted", "category": "Fasteners", "unit": "Kilogram", "quantity_on_hand": 300, "unit_price": 95.00},
    {"item_code": "MAT-014", "material_name": "Concrete Mix", "category": "Construction Materials", "unit": "Bag", "quantity_on_hand": 500, "unit_price": 195.00},
    {"item_code": "MAT-015", "material_name": "Glass Plain 4mm", "category": "Windows & Doors", "unit": "Square Meter", "quantity_on_hand": 80, "unit_price": 450.00},
    {"item_code": "MAT-016", "material_name": "Door Hinges Heavy Duty", "category": "Hardware", "unit": "Piece", "quantity_on_hand": 400, "unit_price": 125.00},
    {"item_code": "MAT-017", "material_name": "Light Fixtures LED", "category": "Electrical", "unit": "Unit", "quantity_on_hand": 150, "unit_price": 850.00},
    {"item_code": "MAT-018", "material_name": "Waterproofing Membrane", "category": "Construction Materials", "unit": "Roll", "quantity_on_hand": 60, "unit_price": 1200.00},
    {"item_code": "MAT-019", "material_name": "Insulation Foam", "category": "Insulation", "unit": "Sheet", "quantity_on_hand": 100, "unit_price": 350.00},
    {"item_code": "MAT-020", "material_name": "Faucets Standard", "category": "Plumbing", "unit": "Unit", "quantity_on_hand": 85, "unit_price": 280.00},
    {"item_code": "MAT-021", "material_name": "Circuit Breakers 20A", "category": "Electrical", "unit": "Piece", "quantity_on_hand": 120, "unit_price": 185.00},
    {"item_code": "MAT-022", "material_name": "Wall Putty", "category": "Finishing Materials", "unit": "Bag", "quantity_on_hand": 250, "unit_price": 145.00},
    {"item_code": "MAT-023", "material_name": "Adhesive Tile", "category": "Finishing Materials", "unit": "Bag", "quantity_on_hand": 180, "unit_price": 165.00},
    {"item_code": "MAT-024", "material_name": "Lumber 2x4x10", "category": "Wood & Lumber", "unit": "Piece", "quantity_on_hand": 300, "unit_price": 325.00},
    {"item_code": "MAT-025", "material_name": "Conduit Pipes", "category": "Electrical", "unit": "Length", "quantity_on_hand": 400, "unit_price": 65.00},
]

# Create inventory items
for data in inventory_data:
    item, created = InventoryItem.objects.get_or_create(
        item_code=data["item_code"],
        defaults=data
    )
    if created:
        print(f"Created: {item.item_code} - {item.material_name}")
    else:
        print(f"Already exists: {item.item_code}")

print(f"\nTotal items in inventory: {InventoryItem.objects.count()}")
