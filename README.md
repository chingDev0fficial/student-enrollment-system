# Student Enrollment System

A comprehensive web-based application for managing student enrollments built with Django and Bootstrap.

![Student Enrollment System](https://github.com/yourusername/student-enrollment-system/raw/main/screenshots/dashboard.png)

## Overview

The Student Enrollment System is a web application designed to simplify the process of student registration and management. It provides an intuitive interface for students to submit their enrollment information and for administrators to manage student records.

## Features

### For Students

- **User-Friendly Enrollment Form**: Simple and intuitive form for students to submit their personal, educational, and family information
- **Form Validation**: Client-side and server-side validation to ensure data integrity
- **Success Confirmation**: Clear confirmation when enrollment is successfully processed

### For Administrators

- **Secure Admin Dashboard**: Password-protected administrative interface for managing student data
- **Comprehensive Student Management**:
  - View complete student details
  - Update student information
  - Delete student records
- **Powerful Search**: Quick search functionality to find students by name, email, or school
- **Role-Based Access Control**: Different permission levels for administrators and moderators

## Technology Stack

### Backend

- **Django (5.2)**: High-level Python web framework for rapid development
- **Django REST Framework**: For potential API functionality
- **Python 3.8+**: Core programming language

### Frontend

- **HTML5/CSS3**: For structure and styling
- **Bootstrap 5**: Responsive front-end framework
- **JavaScript**: For interactive elements
- **Bootstrap Icons**: For visual elements and iconography

### Form Handling

- **django-crispy-forms**: For elegant Django form rendering
- **crispy-bootstrap5**: Bootstrap 5 template pack for crispy-forms

### Database

- **SQLite**: For development environment
- **Neon PostgreSQL**: For production environment

### Deployment

- **Render**: Cloud platform for web service hosting
- **Whitenoise**: Static file serving for Django applications
- **Gunicorn**: WSGI HTTP Server for deploying Django applications

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Local Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/student-enrollment-system.git
   cd student-enrollment-system
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following variables:

   ```
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Visit `http://127.0.0.1:8000` in your browser to access the application.

## Usage

### Student Enrollment

1. Navigate to the home page and click "Enroll Now"
2. Fill out the enrollment form with personal information, parent/guardian details, and academic background
3. Submit the form to complete the enrollment process

### Admin Management

1. Login to the admin dashboard via the login button in the navbar
2. View the list of enrolled students
3. Use the search functionality to find specific students
4. Click on individual student entries to view detailed information
5. Use the provided buttons to edit or delete student records as needed

## Deployment to Production

This project is configured for deployment on Render using Neon PostgreSQL for database management.

### Neon PostgreSQL Setup

1. Create an account on [Neon](https://neon.tech)
2. Create a new project and PostgreSQL database
3. Note the connection string provided by Neon, which will look like:
   ```
   postgresql://username:password@endpoint-url/database_name?sslmode=require
   ```

### Render Deployment

1. Create an account on [Render](https://render.com)
2. Create a new Web Service and connect your GitHub repository
3. Configure the service with the following settings:

   - **Name**: student-enrollment-system (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command**: `gunicorn student_enrollment.wsgi:application`

4. Add the following environment variables:

   - `DJANGO_SECRET_KEY`: A secure random key
   - `DJANGO_DEBUG`: False
   - `DJANGO_ALLOWED_HOSTS`: your-app-name.onrender.com
   - `DATABASE_URL`: Your Neon PostgreSQL connection string

5. Deploy the service and monitor the build logs for any issues

### Security Considerations for Production

The project is configured with security settings that are automatically enabled in production:

- HTTPS enforcement
- Secure cookies
- HTTP Strict Transport Security (HSTS)
- Content security headers

## Project Structure

```
student_enrollment/
├── enrollment/              # Main application
│   ├── admin.py             # Admin interface configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Database models
│   ├── templates/           # HTML templates
│   ├── tests.py             # Test cases
│   ├── urls.py              # URL routing
│   └── views.py             # View controllers
├── static/                  # Static assets
│   ├── css/                 # CSS stylesheets
│   └── js/                  # JavaScript files
├── templates/               # Base templates
├── student_enrollment/      # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Project URL routing
│   └── wsgi.py              # WSGI configuration
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Render](https://render.com)
- [Neon PostgreSQL](https://neon.tech)
