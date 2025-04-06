from django.db import models
from django.urls import reverse


class Student(models.Model):
    """Model representing a student enrollment record."""

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    address = models.TextField()
    parent_information = models.TextField(help_text="Include parent's name, contact number, and relationship")
    school_name_graduated = models.CharField(max_length=200)

    # Metadata
    date_enrolled = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_enrolled"]

    def __str__(self):
        """String representation of the Student."""
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this student."""
        return reverse("enrollment:student-detail", args=[str(self.id)])

    def get_full_name(self):
        """Returns the student's full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
