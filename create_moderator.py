#!/usr/bin/env python
# Script to create a moderator user for the Student Enrollment System.

import os
import django
import sys

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_enrollment.settings")
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from enrollment.models import Student


def create_moderator(username, email, password):
    # Create a new moderator user with appropriate permissions.
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,  # Not staff (can't access admin site)
            is_superuser=False,  # Not superuser
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
    if len(sys.argv) != 4:
        print("Usage: python create_moderator.py <username> <email> <password>")
        sys.exit(1)

    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]

    create_moderator(username, email, password)
    print("Done!")
