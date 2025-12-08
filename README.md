# Demo ERP System

A simple, functional Enterprise Resource Planning (ERP) system built with Flask. This demo application provides core ERP functionalities including customer management, product inventory, and order processing.

## Features

- **Dashboard**: Overview of key metrics and recent orders
- **Customer Management**: Add, edit, view, and delete customer records
- **Product Management**: Manage product inventory with pricing and stock levels
- **Order Management**: Create and track orders with automatic inventory updates
- **Real-time Status Updates**: Update order status dynamically
- **Responsive Design**: Modern UI built with Bootstrap 5

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rickyaguilar/erp-system.git
cd erp-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

The database will be automatically created on first run.

## Usage

### Dashboard
The main dashboard provides an overview of:
- Total number of customers
- Total number of products
- Total number of orders
- Recent orders list

### Managing Customers
1. Click "Customers" in the sidebar
2. Click "Add Customer" to create a new customer
3. Fill in customer details (name, email, phone, address)
4. Use Edit/Delete buttons to modify or remove customers

### Managing Products
1. Click "Products" in the sidebar
2. Click "Add Product" to create a new product
3. Enter product details (name, description, price, quantity)
4. Products with low stock are highlighted
5. Use Edit/Delete buttons to modify or remove products

### Creating Orders
1. Click "Orders" in the sidebar
2. Click "Create Order"
3. Select a customer and product
4. Enter quantity (system validates against available stock)
5. Total price is calculated automatically
6. Order status can be updated directly from the orders list

## Project Structure

```
erp-system/
├── app.py                 # Main application file with routes and models
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Dashboard
│   ├── customers.html   # Customer list
│   ├── add_customer.html
│   ├── edit_customer.html
│   ├── products.html    # Product list
│   ├── add_product.html
│   ├── edit_product.html
│   ├── orders.html      # Order list
│   └── add_order.html
└── instance/            # Database storage (created on first run)
    └── erp_demo.db
```

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, Bootstrap Icons
- **Template Engine**: Jinja2

## Features in Detail

### Customer Management
- Full CRUD operations
- Email validation
- Customer order history tracking

### Product Management
- Inventory tracking
- Price management
- Stock level indicators
- Automatic stock updates on order creation

### Order Management
- Multi-step order creation
- Automatic price calculation
- Stock validation
- Order status workflow (Pending → Processing → Shipped → Completed)
- Order cancellation option

## Database Schema

The application uses SQLite with three main tables:

- **Customer**: id, name, email, phone, address, created_at
- **Product**: id, name, description, price, quantity, created_at
- **Order**: id, customer_id, product_id, quantity, total_price, status, created_at

## Security Notes

⚠️ **Important**: This is a demo application. For production use, you should:
- Change the SECRET_KEY in app.py
- Use a production-grade database (PostgreSQL, MySQL)
- Add user authentication and authorization
- Implement input validation and sanitization
- Add CSRF protection
- Use environment variables for configuration
- Enable HTTPS

## License

This is a demo project for educational purposes.