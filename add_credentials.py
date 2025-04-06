#!/usr/bin/env python
# Script to create admin users for the Student Enrollment System.

import os
import django
import sys

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_enrollment.settings")
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from enrollment.models import Student


def create_superadmin(username, email, password):
    """Create a superadmin user with full access to the system."""
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")

        # Ensure the user is a superadmin
        if not user.is_superuser or not user.is_staff:
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"User '{username}' has been upgraded to superadmin status.")
    else:
        # Create new superadmin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,  # Can access admin site
            is_superuser=True,  # Has all permissions
        )
        print(f"Superadmin '{username}' created successfully.")

    return user


def create_moderator(username, email, password):
    """Create a moderator user with limited admin access."""
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")

        # Ensure the user has staff status
        if not user.is_staff:
            user.is_staff = True
            user.is_superuser = False
            user.save()
            print(f"User '{username}' has been granted staff status.")
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,  # Can access admin site
            is_superuser=False,  # No superuser privileges
        )
        print(f"User '{username}' created successfully.")

    # Add moderator permission
    content_type = ContentType.objects.get_for_model(Student)
    moderator_permission = Permission.objects.get(codename="moderator_access", content_type=content_type)

    if moderator_permission in user.user_permissions.all():
        print(f"User '{username}' already has moderator permissions.")
    else:
        user.user_permissions.add(moderator_permission)
        print(f"Moderator permissions granted to '{username}'.")

    return user


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create moderator: python add_credentials.py moderator <username> <email> <password>")
        print("  Create superadmin: python add_credentials.py superadmin <username> <email> <password>")
        sys.exit(1)

    user_type = sys.argv[1].lower()

    if user_type not in ["moderator", "superadmin"]:
        print("Error: First argument must be either 'moderator' or 'superadmin'")
        sys.exit(1)

    if len(sys.argv) != 5:
        print(f"Usage: python add_credentials.py {user_type} <username> <email> <password>")
        sys.exit(1)

    username = sys.argv[2]
    email = sys.argv[3]
    password = sys.argv[4]

    if user_type == "moderator":
        create_moderator(username, email, password)
    else:
        create_superadmin(username, email, password)

    print("Done!")
