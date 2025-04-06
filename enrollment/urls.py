from django.urls import path
from . import views

app_name = "enrollment"

urlpatterns = [
    # Landing page
    path("", views.index, name="index"),
    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Student enrollment
    path("enroll/", views.enroll_student, name="enroll"),
    path("enrollment-success/", views.enrollment_success, name="enrollment-success"),
    # Changed from admin/ to dashboard/ to avoid conflict with Django admin
    path("dashboard/", views.admin_dashboard, name="admin-dashboard"),
    path("dashboard/student/<int:pk>/", views.student_detail, name="student-detail"),
    path("dashboard/student/<int:pk>/update/", views.update_student, name="student-update"),
    path("dashboard/student/<int:pk>/delete/", views.delete_student, name="student-delete"),
    path("dashboard/search/", views.search_students, name="search-students"),
]
