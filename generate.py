from django.contrib.auth.hashers import make_password
from django.conf import settings
import os

# Configure Django settings before using make_password
settings.configure(
    PASSWORD_HASHERS=[
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    ],
    SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY"),
)

print(make_password("password123"))
