from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from .models import Student


class DateInput(forms.DateInput):
    """Custom DateInput widget with HTML5 date input type."""

    input_type = "date"


class StudentForm(forms.ModelForm):
    """Form for creating and updating Student records."""

    class Meta:
        model = Student
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "birthday",
            "address",
            "parent_information",
            "school_name_graduated",
        ]
        widgets = {
            "birthday": DateInput(),
            "address": forms.Textarea(attrs={"rows": 3}),
            "parent_information": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Enter first name"})
        self.fields["middle_name"].widget.attrs.update({"class": "form-control", "placeholder": "Enter middle name (optional)"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Enter last name"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter email address"})
        self.fields["birthday"].widget.attrs.update({"class": "form-control"})
        self.fields["address"].widget.attrs.update({"class": "form-control", "placeholder": "Enter complete address"})
        self.fields["parent_information"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter parent's name, contact number, and relationship",
            }
        )
        self.fields["school_name_graduated"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter school name where you graduated",
            }
        )

        # Setup crispy form helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-3"
        self.helper.field_class = "col-lg-9"
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="form-group col-md-4 mb-3"),
                Column("middle_name", css_class="form-group col-md-4 mb-3"),
                Column("last_name", css_class="form-group col-md-4 mb-3"),
                css_class="form-row",
            ),
            "email",
            "birthday",
            "address",
            "parent_information",
            "school_name_graduated",
            Div(
                Submit("submit", "Submit Enrollment", css_class="btn btn-primary"),
                css_class="text-center mt-4",
            ),
        )

    def clean_email(self):
        """Validate that the email is not already in use."""
        email = self.cleaned_data.get("email")
        if Student.objects.filter(email=email).exists() and not self.instance.pk:
            raise ValidationError("This email is already registered in our system.")
        return email

    def clean_birthday(self):
        """Additional validation for birthday field."""
        birthday = self.cleaned_data.get("birthday")
        # Add any additional validation for birthdate if needed
        return birthday
