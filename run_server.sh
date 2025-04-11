#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "${SCRIPT_DIR}/script_helper.sh" || { echo "Failed to source helper script"; exit 1; }

check_requirements python pip

set -e

deactivate 2>/dev/null || true

print_header "Django Development Server Setup"

if [ ! -d ".venv" ]; then
    log_message "Creating virtual environment..."
    python -m venv .venv || handle_error "Failed to create virtual environment"
fi

activate_venv

if [ -f "requirements-dev.txt" ]; then
    log_message "Installing dependencies from requirements-dev.txt..."
    pip install -r requirements-dev.txt || handle_error "Failed to install requirements from requirements-dev.txt"
elif [ -f "requirements.txt" ]; then
    log_message "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt || handle_error "Failed to install dependencies from requirements.txt"
else
    log_message "No requirements file found, skipping dependency installation."
fi

log_message "Building static files..."
python manage.py collectstatic --noinput || handle_error "Failed to collect static files"

log_message "Running migrations..."
python manage.py makemigrations || handle_error "Failed to make migrations"
python manage.py migrate || handle_error "Failed to apply migrations"

print_header "Starting Django Development Server"
log_message "Server is now running. Press CTRL+C to stop."
python manage.py runserver 0.0.0.0:8000 || handle_error "Failed to start development server"
