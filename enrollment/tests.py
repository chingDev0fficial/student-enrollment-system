from django.test import TestCase, Client
from django.urls import reverse
from .models import Student
from datetime import date


class StudentModelTest(TestCase):
    """Tests for the Student model."""

    def setUp(self):
        """Create a sample student record for testing."""
        self.student = Student.objects.create(
            first_name="John",
            middle_name="Robert",
            last_name="Doe",
            email="john.doe@example.com",
            birthday=date(2000, 1, 15),
            address="123 Main St, Anytown",
            parent_information="Mary Doe, 555-123-4567, Mother",
            school_name_graduated="Anytown High School",
        )

    def test_student_creation(self):
        """Test that we can create a student record."""
        self.assertEqual(self.student.first_name, "John")
        self.assertEqual(self.student.email, "john.doe@example.com")

    def test_get_full_name(self):
        """Test the get_full_name method."""
        self.assertEqual(self.student.get_full_name(), "John Robert Doe")

        # Test without middle name
        self.student.middle_name = ""
        self.student.save()
        self.assertEqual(self.student.get_full_name(), "John Doe")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method."""
        expected_url = reverse("enrollment:student-detail", args=[self.student.id])
        self.assertEqual(self.student.get_absolute_url(), expected_url)


class EnrollmentViewsTest(TestCase):
    """Tests for enrollment views."""

    def setUp(self):
        """Initialize the test client."""
        self.client = Client()

    def test_index_view(self):
        """Test the index view."""
        response = self.client.get(reverse("enrollment:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "enrollment/index.html")

    def test_enrollment_form_view_get(self):
        """Test the enrollment form view (GET)."""
        response = self.client.get(reverse("enrollment:enroll"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "enrollment/enroll.html")
        self.assertContains(response, "Student Enrollment Form")

    def test_enrollment_form_submission(self):
        """Test submission of the enrollment form."""
        # Data for form submission
        data = {
            "first_name": "Jane",
            "middle_name": "Mary",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "birthday": "2001-05-20",
            "address": "456 Oak St, Somewhere",
            "parent_information": "John Smith, 555-987-6543, Father",
            "school_name_graduated": "Somewhere High School",
        }

        # Submit the form
        response = self.client.post(reverse("enrollment:enroll"), data)

        # Check that we're redirected to success page
        self.assertRedirects(response, reverse("enrollment:enrollment-success"))

        # Check that a student was created in the database
        self.assertTrue(Student.objects.filter(email="jane.smith@example.com").exists())

    def test_admin_dashboard_view(self):
        """Test the admin dashboard view."""
        # Create some test students
        Student.objects.create(
            first_name="Alice",
            last_name="Johnson",
            email="alice@example.com",
            birthday=date(2000, 3, 10),
            address="789 Pine St, Elsewhere",
            parent_information="Bob Johnson, 555-111-2222, Father",
            school_name_graduated="Elsewhere High School",
        )

        # Access the dashboard
        response = self.client.get(reverse("enrollment:admin-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "enrollment/dashboard.html")

        # Check that the student is in the context
        self.assertTrue(len(response.context["students"]) > 0)

    def test_search_functionality(self):
        """Test the search functionality."""
        # Create test students
        Student.objects.create(
            first_name="Michael",
            last_name="Brown",
            email="michael@example.com",
            birthday=date(1999, 8, 15),
            address="101 Maple Ave, Nowhereville",
            parent_information="Sarah Brown, 555-333-4444, Mother",
            school_name_graduated="Central High School",
        )

        Student.objects.create(
            first_name="Emily",
            last_name="Davis",
            email="emily@example.com",
            birthday=date(2002, 12, 1),
            address="202 Elm St, Anyplace",
            parent_information="David Davis, 555-555-6666, Father",
            school_name_graduated="Eastside High School",
        )

        # Search by first name
        response = self.client.get(reverse("enrollment:search-students") + "?q=Michael")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["students"]), 1)

        # Search by school name
        response = self.client.get(reverse("enrollment:search-students") + "?q=Eastside")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["students"]), 1)
        self.assertEqual(response.context["students"][0].first_name, "Emily")
