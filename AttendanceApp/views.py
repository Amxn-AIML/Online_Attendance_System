import random
import math
import base64
import uuid
from datetime import timedelta

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from django.db.models import Count, Max

from .models import Student, Attendance, AttendanceLocation
from .face_utils import match_face
from allauth.socialaccount.models import SocialAccount


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000

    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))

    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lon2) - float(lon1))

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2) ** 2
    )

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def reset_location_if_new_day():
    AttendanceLocation.objects.filter(
        is_active=True,
        created_at__lt=now() - timedelta(hours=12)
    ).update(is_active=False)


def send_student_otp(student, request):

    otp = random.randint(100000, 999999)

    request.session["otp"] = otp
    request.session["otp_expiry"] = (
        now() + timedelta(minutes=2)
    ).timestamp()

    request.session["student_id"] = student.id

    send_mail(
        subject="Your OTP Verification Code | Online Attendance System",

        message=f"""
Hello {student.name},

Welcome to Online Attendance System.

Your One Time Password (OTP) for secure login is:

🔐 {otp}

This OTP is valid for only 2 minutes.

Please do not share this code with anyone.

If you did not request this login, you can ignore this email.

Regards,
Online Attendance Team
""",

        from_email="attendence0101@gmail.com",
        recipient_list=[student.email],
        fail_silently=True
    )


def login_view(request):

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        try:
            student = Student.objects.get(
                email=email,
                password=password
            )

        except Student.DoesNotExist:

            return render(request, "login.html", {
                "error": "Invalid credentials"
            })

        request.session["student_id"] = student.id

        if student.is_verified:
            return redirect("/student-dashboard/")

        send_student_otp(student, request)

        return redirect("/otp/")

    return render(request, "login.html")


def resend_otp(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("/")

    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return redirect("/")

    send_student_otp(student, request)

    request.session["otp_resent"] = True

    return redirect("/otp/")


def otp_view(request):

    if request.method == "GET":
        return render(request, "otp.html")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        session_otp = request.session.get("otp")
        expiry = request.session.get("otp_expiry")

        student_id = request.session.get("student_id")

        if not session_otp or not expiry:

            return render(request, "otp.html", {
                "error": "Session expired"
            })

        if now().timestamp() > expiry:

            return render(request, "otp.html", {
                "error": "OTP expired. Please resend OTP."
            })

        if str(entered_otp) == str(session_otp):

            try:
                student = Student.objects.get(id=student_id)

                student.is_verified = True
                student.save()

            except Student.DoesNotExist:
                return redirect("/")

            request.session.pop("otp", None)
            request.session.pop("otp_expiry", None)
            request.session.pop("otp_resent", None)

            return redirect("/student-dashboard/")

        return render(request, "otp.html", {
            "error": "Invalid OTP"
        })


def student_dashboard(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("/")

    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return redirect("/")

    total_attendance = Attendance.objects.filter(
        student=student,
        status="PRESENT"
    ).count()

    last_attendance = Attendance.objects.filter(
        student=student
    ).order_by("-date", "-time").first()

    today_marked = Attendance.objects.filter(
        student=student,
        date=now().date(),
        status="PRESENT"
    ).exists()

    return render(request, "student_dashboard.html", {
        "student": student,
        "total_attendance": total_attendance,
        "last_attendance": last_attendance,
        "today_marked": today_marked
    })


def attendance_view(request):

    reset_location_if_new_day()

    location = AttendanceLocation.objects.filter(
        is_active=True
    ).first()

    if request.method == "POST":

        roll = request.POST.get("roll")

        try:
            student = Student.objects.get(roll=roll)

        except Student.DoesNotExist:

            return render(request, "attendance.html", {
                "error": "Invalid roll number",
                "location_start": location.created_at.timestamp() if location else None
            })

        today = now().date()

        if Attendance.objects.filter(
            student=student,
            date=today,
            status="PRESENT"
        ).exists():

            return render(request, "attendance.html", {
                "error": "Attendance already marked today",
                "location_start": location.created_at.timestamp() if location else None
            })

        image_data = request.POST.get("image_data")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        if not image_data or not latitude or not longitude:

            return render(request, "attendance.html", {
                "error": "Face and location required",
                "location_start": location.created_at.timestamp() if location else None
            })

        if not location:

            return render(request, "attendance.html", {
                "error": "Attendance location not set"
            })

        distance = calculate_distance(
            latitude,
            longitude,
            location.latitude,
            location.longitude
        )

        format, imgstr = image_data.split(";base64,")

        image_file = ContentFile(
            base64.b64decode(imgstr),
            name=f"{uuid.uuid4()}.jpg"
        )

        is_match = match_face(
            image_file,
            student.face_image.path
        )

        if not is_match:

            return render(request, "attendance.html", {
                "error": "Face not recognized",
                "location_start": location.created_at.timestamp()
            })

        if distance > location.radius:

            return render(request, "attendance.html", {
                "error": "Outside allowed location radius",
                "location_start": location.created_at.timestamp()
            })

        Attendance.objects.create(
            student=student,
            latitude=latitude,
            longitude=longitude,
            image=image_file,
            status="PRESENT"
        )

        return redirect("/success/")

    return render(request, "attendance.html", {
        "location_start": location.created_at.timestamp() if location else None
    })


def success_view(request):
    return render(request, "success.html")


def failed_view(request):
    return render(request, "failed.html")


def admin_login(request):

    if request.method == "POST":

        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if user and user.is_staff:

            login(request, user)

            return redirect("/admin-dashboard/")

        return render(request, "admin_login.html", {
            "error": "Invalid admin credentials"
        })

    return render(request, "admin_login.html")


@login_required
def admin_logout(request):

    logout(request)

    return redirect("/admin-login/")


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    reset_location_if_new_day()

    return render(request, "admin.html", {
        "total_students": Student.objects.count(),

        "today_attendance": Attendance.objects.filter(
            date=now().date(),
            status="PRESENT"
        ).count(),

        "total_attendance": Attendance.objects.count(),

        "active_location": AttendanceLocation.objects.filter(
            is_active=True
        ).first()
    })


@login_required
def add_location(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    if request.method == "POST":

        AttendanceLocation.objects.update(
            is_active=False
        )

        AttendanceLocation.objects.create(
            name=request.POST.get("name"),
            latitude=request.POST.get("latitude"),
            longitude=request.POST.get("longitude"),
            radius=request.POST.get("radius"),
            is_active=True
        )

    return redirect("/admin-location/")


@login_required
def students_page(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    if request.method == "POST":

        Student.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            roll=request.POST["roll"],
            password=request.POST["password"],
            face_image=request.FILES["face_image"]
        )

        return redirect("/students/")

    return render(request, "add_student.html", {
        "students": Student.objects.all().order_by("roll")
    })


@login_required
def delete_student(request, student_id):

    if request.user.is_staff:
        Student.objects.filter(id=student_id).delete()

    return redirect("/students/")


@login_required
def admin_student_report(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    students = Student.objects.annotate(
        attendance_count=Count("attendance"),
        last_date=Max("attendance__date"),
        last_time=Max("attendance__time")
    ).order_by("roll")

    return render(request, "admin_student_report.html", {
        "students": students
    })


@login_required
def admin_today_attendance(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    attendance = Attendance.objects.filter(
        date=now().date()
    ).order_by("-time")

    return render(request, "admin_today_attendance.html", {
        "attendance": attendance
    })


@login_required
def admin_absent_students(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    today = now().date()

    present_ids = Attendance.objects.filter(
        date=today,
        status="PRESENT"
    ).values_list("student_id", flat=True)

    students = Student.objects.exclude(
        id__in=present_ids
    ).order_by("roll")

    return render(request, "admin_absent_students.html", {
        "students": students
    })


@login_required
def clear_today_attendance(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    Attendance.objects.filter(
        date=now().date()
    ).delete()

    return redirect("/admin-today-attendance/")


@login_required
def admin_location(request):

    if not request.user.is_staff:
        return redirect("/admin-login/")

    reset_location_if_new_day()

    return render(request, "admin_location.html", {
        "total_students": Student.objects.count(),

        "today_attendance": Attendance.objects.filter(
            date=now().date(),
            status="PRESENT"
        ).count(),

        "total_attendance": Attendance.objects.count(),

        "active_location": AttendanceLocation.objects.filter(
            is_active=True
        ).first()
    })


def clear_location(request):

    if request.method == "POST":
        AttendanceLocation.objects.all().delete()

    return redirect("/admin-location/")

def google_login_redirect(request):

    if request.user.is_authenticated:

        try:

            social_user = SocialAccount.objects.get(user=request.user)

            print(social_user.extra_data)

            email = social_user.extra_data.get("email")

            print("EMAIL:", email)

            student = Student.objects.filter(email=email).first()

            if student:

                request.session["student_id"] = student.id

                return redirect("/student-dashboard/")

            logout(request)

            return redirect("/")

        except Exception as e:

            print("ERROR:", e)

            logout(request)

            return redirect("/")

    return redirect("/")