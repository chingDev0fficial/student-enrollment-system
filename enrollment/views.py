from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from .models import Student
from .forms import StudentForm


def is_moderator(user):
    # Check if user is a moderator or staff.
    if not user.is_authenticated:
        return False
    # Allow either staff users OR users with the specific moderator permission
    return user.is_staff or user.has_perm("enrollment.moderator_access")


# Landing page view
def index(request):
    # Display the landing page.
    return render(request, "../templates/enrollment/index.html")


# Student registration view
def enroll_student(request):
    # Handle student enrollment (both GET and POST requests).
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

    return render(request, "../templates/enrollment/enroll.html", {"form": form})


# Enrollment success view
def enrollment_success(request):
    # Display a success message after successful enrollment.
    return render(request, "../templates/enrollment/enrollment_success.html")


# Authentication views
def login_view(request):
    # Handle user login.
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")

            # Redirect to referring page or dashboard
            next_url = request.POST.get("next", "enrollment:admin-dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(request.META.get("HTTP_REFERER", "enrollment:index"))

    # If not POST, redirect to home
    return redirect("enrollment:index")


def logout_view(request):
    # Handle user logout.
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("enrollment:index")


# Admin dashboard view
@user_passes_test(is_moderator, login_url="enrollment:index")
def admin_dashboard(request):
    # Display the admin dashboard with a list of all students.
    students = Student.objects.all()
    context = {
        "students": students,
        "total_students": students.count(),
    }
    return render(request, "../templates/enrollment/dashboard.html", context)


# Student detail view
@user_passes_test(is_moderator, login_url="enrollment:index")
def student_detail(request, pk):
    # Display details for a specific student.
    student = get_object_or_404(Student, pk=pk)
    return render(request, "../templates/enrollment/student_detail.html", {"student": student})


# Student update view
@user_passes_test(is_moderator, login_url="enrollment:index")
def update_student(request, pk):
    # Handle updates to a student record.
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

    return render(request, "../templates/enrollment/student_update.html", {"form": form, "student": student})


# Student delete view
@user_passes_test(is_moderator, login_url="enrollment:index")
def delete_student(request, pk):
    # Handle deletion of a student record.
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student_name = student.get_full_name()
        student.delete()
        messages.success(request, f"{student_name} has been removed from the system.")
        return redirect("enrollment:admin-dashboard")

    return render(request, "../templates/enrollment/student_delete.html", {"student": student})


# Search view
@user_passes_test(is_moderator, login_url="enrollment:index")
def search_students(request):
    # Search for students based on query parameters.
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

    return render(request, "../templates/enrollment/search.html", context)
