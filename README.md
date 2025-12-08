# ERP System

A simple Django-based Enterprise Resource Planning (ERP) system with authentication and dashboard functionality.

## Features

- **User Authentication**: Secure login/logout system using Django's built-in authentication
- **Dashboard**: Clean, modern dashboard with statistics and quick actions
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Professional UI**: Clean design with Font Awesome icons

## Getting Started

### Prerequisites

- Python 3.x
- Django 5.2.7

### Installation

1. Navigate to the project directory:
   ```bash
   cd /home/riks/projects/erp_system
   ```

2. Run database migrations:
   ```bash
   python3 manage.py migrate
   ```

3. Create a superuser account:
   ```bash
   python3 manage.py createsuperuser
   ```

4. Start the development server:
   ```bash
   python3 manage.py runserver
   ```

5. Open your browser and go to: `http://localhost:8000`

### Default Test Account

A test superuser has been created with the following credentials:
- **Username**: admin
- **Password**: admin123

## Project Structure

```
erp_system/
├── manage.py
├── erp_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── views.py      # Authentication and dashboard views
│   ├── urls.py       # URL routing
│   └── ...
├── templates/
│   ├── base.html                # Base template
│   ├── dashboard.html           # Dashboard page
│   └── registration/
│       └── login.html           # Login page
└── static/
    └── css/
        └── style.css           # Custom CSS styles
```

## Usage

1. **Login**: Navigate to the root URL, and you'll be redirected to the login page if not authenticated
2. **Dashboard**: After successful login, you'll see the main dashboard with:
   - System statistics (users, active sessions)
   - Welcome message and feature overview
   - Quick action buttons (placeholder for future features)
3. **Logout**: Use the logout button in the navigation bar

## Technology Stack

- **Backend**: Django 5.2.7
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Database**: SQLite (default Django setup)
- **Authentication**: Django's built-in user authentication system

## Next Steps

This is a foundation for an ERP system. Future enhancements could include:
- User management module
- Inventory management
- Financial reporting
- Customer relationship management (CRM)
- Human resources management
- Advanced analytics and reporting

## Contributing

This project is set up for incremental development. Each feature should be developed step by step with proper testing.