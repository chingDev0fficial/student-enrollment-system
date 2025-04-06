#!/bin/bash
# Script to create a superuser for the Student Enrollment System
# This script can be used in production environments with PostgreSQL

# Exit on error
set -e

# Help text
show_help() {
    echo "Usage: ./create_superuser.sh [OPTIONS]"
    echo ""
    echo "This script creates a superuser for the Student Enrollment System."
    echo ""
    echo "Options:"
    echo "  -u, --username USERNAME   Superuser username (required)"
    echo "  -e, --email EMAIL         Superuser email (required)"
    echo "  -p, --password PASSWORD   Superuser password (required)"
    echo "  -h, --help                Display this help and exit"
    echo ""
    echo "Example:"
    echo "  ./create_superuser.sh -u admin -e admin@example.com -p securepassword"
}

# Default values
USERNAME="admin"
EMAIL="admin@admin.com"
PASSWORD="password123"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -u|--username)
            USERNAME="$2"
            shift
            shift
            ;;
        -e|--email)
            EMAIL="$2"
            shift
            shift
            ;;
        -p|--password)
            PASSWORD="$2"
            shift
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if required arguments are provided
if [[ -z "$USERNAME" || -z "$EMAIL" || -z "$PASSWORD" ]]; then
    echo "Error: Missing required arguments"
    show_help
    exit 1
fi

# Check if python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not available in PATH"
    exit 1
fi

# Execute the add_credentials.py script to create a superadmin
echo "Creating superuser '$USERNAME'..."
python add_credentials.py superadmin "$USERNAME" "$EMAIL" "$PASSWORD"

# Check execution status
if [ $? -eq 0 ]; then
    echo "Superuser created successfully!"
    exit 0
else
    echo "Failed to create superuser."
    exit 1
fi
```
