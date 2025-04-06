from django.db import models
from django.urls import reverse


class Student(models.Model):
    # Model representing a student enrollment record.

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    address = models.TextField()

    # Detailed parent information fields (replacing parent_information field)
    parent_full_name = models.CharField(max_length=200, null=True, help_text="Full name of parent or guardian")
    relationship = models.CharField(
        max_length=50, null=True, help_text="Relationship to student (e.g., Father, Mother, Guardian)"
    )
    parent_phone = models.CharField(max_length=20, null=True, help_text="Parent's primary phone number")
    parent_email = models.EmailField(blank=True, null=True, help_text="Parent's email address")
    parent_occupation = models.CharField(max_length=100, blank=True, null=True, help_text="Parent's occupation")
    parent_workplace = models.CharField(max_length=200, blank=True, null=True, help_text="Parent's workplace or company name")
    parent_address = models.TextField(blank=True, null=True, help_text="Parent's address if different from student")
    alternate_contact = models.CharField(max_length=20, blank=True, null=True, help_text="Alternative contact number (optional)")

    school_name_graduated = models.CharField(max_length=200)

    # Metadata
    date_enrolled = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_enrolled"]
        permissions = [
            ("moderator_access", "Can access moderator features"),
        ]

    def __str__(self):
        # String representation of the Student.
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        # Returns the URL to access a detail record for this student.
        return reverse("enrollment:student-detail", args=[str(self.id)])

    def get_full_name(self):
        # Returns the student's full name.
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
