from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Student
from .forms import StudentForm


# Landing page view
def index(request):
    """Display the landing page."""
    return render(request, "enrollment/index.html")


# Student registration view
def enroll_student(request):
    """Handle student enrollment (both GET and POST requests)."""
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student enrolled successfully!")
            return redirect("enrollment:enrollment-success")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentForm()

    return render(request, "enrollment/enroll.html", {"form": form})


# Enrollment success view
def enrollment_success(request):
    """Display a success message after successful enrollment."""
    return render(request, "enrollment/enrollment_success.html")


# Admin dashboard view
def admin_dashboard(request):
    """Display the admin dashboard with a list of all students."""
    students = Student.objects.all()
    context = {
        "students": students,
        "total_students": students.count(),
    }
    return render(request, "enrollment/dashboard.html", context)


# Student detail view
def student_detail(request, pk):
    """Display details for a specific student."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, "enrollment/student_detail.html", {"student": student})


# Student update view
def update_student(request, pk):
    """Handle updates to a student record."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Information for {student.get_full_name()} updated successfully!",
            )
            return redirect("enrollment:student-detail", pk=student.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentForm(instance=student)

    return render(request, "enrollment/student_update.html", {"form": form, "student": student})


# Student delete view
def delete_student(request, pk):
    """Handle deletion of a student record."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student_name = student.get_full_name()
        student.delete()
        messages.success(request, f"{student_name} has been removed from the system.")
        return redirect("enrollment:admin-dashboard")

    return render(request, "enrollment/student_delete.html", {"student": student})


# Search view
def search_students(request):
    """Search for students based on query parameters."""
    query = request.GET.get("q", "")
    students = []

    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(school_name_graduated__icontains=query)
        )

    context = {
        "students": students,
        "query": query,
        "total_results": students.count() if query else 0,
    }

    return render(request, "enrollment/search.html", context)
