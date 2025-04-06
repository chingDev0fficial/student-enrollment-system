# Deployment Guide for Student Enrollment System

This document outlines the steps to deploy the Student Enrollment System to a production environment.

## Prerequisites

- A hosting provider (e.g., Heroku, DigitalOcean, AWS, etc.)
- Git repository with your code
- Domain name (optional but recommended)

## Deployment Steps

### 1. Prepare Your Environment Variables

Create a `.env` file based on the provided `.env.example` file and set appropriate values for your production environment:

```
DJANGO_SECRET_KEY=<generate-a-secure-random-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Install Production Requirements

```bash
pip install -r requirements-prod.txt
```

### 3. Configure Static Files

Run the collectstatic command to gather all static files into the STATIC_ROOT directory:

```bash
python manage.py collectstatic --no-input
```

### 4. Test Your Production Settings Locally

```bash
# Set environment variables
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Run the server
python manage.py runserver
```

### 5. Set Up a Production Database (Optional)

If using PostgreSQL instead of SQLite:

```bash
# Example for PostgreSQL
export DATABASE_URL=postgres://user:password@host:port/database
```

### 6. Deploy to Your Hosting Provider

#### Heroku Deployment

1. Install Heroku CLI and login

   ```bash
   heroku login
   ```

2. Create a new Heroku app

   ```bash
   heroku create your-app-name
   ```

3. Add PostgreSQL add-on

   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Configure environment variables

   ```bash
   heroku config:set DJANGO_SECRET_KEY=<your-secret-key>
   heroku config:set DJANGO_DEBUG=False
   heroku config:set DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. Push to Heroku

   ```bash
   git push heroku main
   ```

6. Run migrations
   ```bash
   heroku run python manage.py migrate
   ```

#### DigitalOcean App Platform

1. Create a new app on the DigitalOcean App Platform
2. Connect to your GitHub repository
3. Configure environment variables in the App Platform settings
4. Deploy the app

### 7. Set Up a Custom Domain (Optional)

Follow your hosting provider's instructions to set up a custom domain for your application.

### 8. Monitor Your Application

- Set up error tracking with a service like Sentry
- Monitor application performance
- Check logs regularly for any issues

## Post-Deployment Tasks

1. Create a superuser for the Django admin

   ```bash
   python manage.py createsuperuser
   ```

2. Regularly back up your database
3. Keep dependencies updated to address security vulnerabilities
4. Consider setting up CI/CD for automated testing and deployment
