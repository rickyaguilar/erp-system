"""
Demo ERP System - Main Application
A simple Enterprise Resource Planning system for managing customers, products, and orders.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-erp-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref='orders')

    def __repr__(self):
        return f'<Order {self.id}>'


# Routes
@app.route('/')
def index():
    """Dashboard with overview statistics"""
    customers_count = Customer.query.count()
    products_count = Product.query.count()
    orders_count = Order.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         customers_count=customers_count,
                         products_count=products_count,
                         orders_count=orders_count,
                         recent_orders=recent_orders)


# Customer Routes
@app.route('/customers')
def customers():
    """List all customers"""
    all_customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template('customers.html', customers=all_customers)


@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    """Add a new customer"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        new_customer = Customer(name=name, email=email, phone=phone, address=address)
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')


@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    """Edit an existing customer"""
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('edit_customer.html', customer=customer)


@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    """Delete a customer"""
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customers'))


# Product Routes
@app.route('/products')
def products():
    """List all products"""
    all_products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('products.html', products=all_products)


@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """Add a new product"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            quantity = int(request.form.get('quantity'))
            
            if price < 0 or quantity < 0:
                flash('Price and quantity must be positive values!', 'danger')
                return redirect(url_for('add_product'))
            
            new_product = Product(name=name, description=description, price=price, quantity=quantity)
            db.session.add(new_product)
            db.session.commit()
            
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except (ValueError, TypeError):
            flash('Invalid input. Please check your values!', 'danger')
            return redirect(url_for('add_product'))
    
    return render_template('add_product.html')


@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    """Edit an existing product"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            price = float(request.form.get('price'))
            quantity = int(request.form.get('quantity'))
            
            if price < 0 or quantity < 0:
                flash('Price and quantity must be positive values!', 'danger')
                return redirect(url_for('edit_product', id=id))
            
            product.price = price
            product.quantity = quantity
            
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        except (ValueError, TypeError):
            flash('Invalid input. Please check your values!', 'danger')
            return redirect(url_for('edit_product', id=id))
    
    return render_template('edit_product.html', product=product)


@app.route('/products/delete/<int:id>')
def delete_product(id):
    """Delete a product"""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))


# Order Routes
@app.route('/orders')
def orders():
    """List all orders"""
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=all_orders)


@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    """Add a new order"""
    if request.method == 'POST':
        try:
            customer_id = int(request.form.get('customer_id'))
            product_id = int(request.form.get('product_id'))
            quantity = int(request.form.get('quantity'))
            
            if quantity <= 0:
                flash('Quantity must be a positive number!', 'danger')
                return redirect(url_for('add_order'))
            
            product = Product.query.get(product_id)
            if not product:
                flash('Product not found!', 'danger')
                return redirect(url_for('add_order'))
            
            # Validate stock availability
            if product.quantity < quantity:
                flash(f'Insufficient stock! Only {product.quantity} units available.', 'danger')
                return redirect(url_for('add_order'))
            
            total_price = product.price * quantity
            
            new_order = Order(customer_id=customer_id, product_id=product_id, 
                             quantity=quantity, total_price=total_price)
            db.session.add(new_order)
            
            # Update product quantity
            product.quantity -= quantity
            
            db.session.commit()
            flash('Order created successfully!', 'success')
            return redirect(url_for('orders'))
        except (ValueError, TypeError):
            flash('Invalid input. Please check your values!', 'danger')
            return redirect(url_for('add_order'))
    
    customers = Customer.query.all()
    products = Product.query.filter(Product.quantity > 0).all()
    return render_template('add_order.html', customers=customers, products=products)


@app.route('/orders/update/<int:id>', methods=['POST'])
def update_order_status(id):
    """Update order status"""
    order = Order.query.get_or_404(id)
    status = request.form.get('status')
    order.status = status
    db.session.commit()
    
    flash('Order status updated successfully!', 'success')
    return redirect(url_for('orders'))


# Initialize database
def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
