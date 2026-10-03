from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view,name='login'),
    path('otp/', views.otp_view,name='otp'),
    path('attendance/', views.attendance_view,name='attendance'),
    path('success/', views.success_view,name='success'),
    path('admin-dashboard/', views.admin_dashboard,name='admin-dashboard'),
    path('logout/', views.admin_logout,name='logout'),
    path('delete-student/<int:student_id>/', views.delete_student,name='delete'),
    path('admin-login/',views.admin_login,name='admin-login'),
    path('failed/',views.failed_view,name='failed'),
    path('admin-location/',views.admin_location,name='admin-location'),
    path("add-location/", views.add_location),
    path("students/", views.students_page),
    path('admin-student-report/',views.admin_student_report),
    path('admin-today-attendance/',views.admin_today_attendance),
    path("clear-today-attendance/", views.clear_today_attendance, name="clear_today_attendance"),
    path("clear-location/", views.clear_location, name="clear_location"),
    path('resend-otp/', views.resend_otp),
    path('admin-absent-students/', views.admin_absent_students),
    path('student-dashboard/', views.student_dashboard),
    path('google-success/',views.google_login_redirect),
]
