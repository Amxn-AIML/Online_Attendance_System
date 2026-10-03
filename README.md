# 📱 Smart Attendance System

###  Online Attendance System using OTP, GPS & Face Recognition

A secure and intelligent **web-based attendance management system** built with **Django** that allows students to mark attendance directly from their smartphones. The system verifies the student's identity using **OTP and Face Recognition** and validates their physical presence using **GPS-based location verification**.

---

## 🚀 Project Overview

Traditional attendance systems can be time-consuming and are vulnerable to proxy attendance.

This project provides a **phone-only digital attendance solution** where a student can mark attendance without requiring a fingerprint scanner, RFID card, or dedicated attendance machine.

### Attendance Verification Flow

```text
Student Login
      ↓
OTP Verification
      ↓
GPS Location Verification
      ↓
Mobile Camera
      ↓
Face Recognition
      ↓
Attendance Validation
      ↓
Attendance Stored in Database
```

---

## ✨ Key Features

### 👨‍🎓 Student Features

* 🔐 Secure student login
* 📩 OTP-based verification
* 📍 GPS location verification
* 📷 Face recognition using mobile camera
* 🕒 Automatic attendance date & time
* ✅ Attendance success/failure feedback
* 📊 Student-specific attendance records
* 📱 Mobile-friendly interface
* 🌐 Works directly through a web browser

### 👨‍💼 Admin Features

* 🔑 Secure admin login
* 👨‍🎓 Add and manage students
* 🗑️ Delete student records
* 📍 Add attendance locations
* 🎯 Configure allowed GPS radius
* 📋 View student attendance reports
* 📅 View today's attendance
* 🧹 Clear today's attendance
* 📊 Manage attendance data

---

## 🧠 Technologies Used

| Technology          | Purpose                       |
| ------------------- | ----------------------------- |
| 🐍 Python           | Backend programming           |
| 🌐 Django           | Web framework                 |
| 🗄️ SQLite / MySQL  | Database                      |
| HTML5               | Frontend structure            |
| CSS3                | UI styling                    |
| JavaScript          | Client-side functionality     |
| 📍 Geolocation API  | GPS verification              |
| 📷 Camera API       | Face image capture            |
| 🤖 Face Recognition | Student identity verification |
| 🔐 OTP              | User verification             |

---

## 🏗️ System Architecture

```text
                ┌─────────────────────┐
                │   Student Mobile    │
                │      Browser        │
                └──────────┬──────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Student Login  │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ OTP Verification│
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ GPS Verification│
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Face Recognition│
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Django Backend │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │    Database    │
                  └────────────────┘
```

---

## 📂 Project Structure

```text
Attendance-System/
│
├── manage.py
│
├── Attendanceproject/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── attendance/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── templates/
│   ├── login.html
│   ├── otp.html
│   ├── attendance.html
│   ├── success.html
│   ├── failed.html
│   ├── admin-login.html
│   ├── admin-dashboard.html
│   ├── students.html
│   ├── admin-location.html
│   ├── admin-student-report.html
│   └── admin-today-attendance.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ How It Works

## 1️⃣ Student Login

The student enters their registered credentials.

```text
Student → Login → Authentication
```

---

## 2️⃣ OTP Verification

For verification, an OTP is sent to the student's registered email.

The OTP has a limited validity period.

```text
Email
  ↓
Generate OTP
  ↓
Send OTP
  ↓
Student enters OTP
  ↓
OTP Verified
```

---

## 3️⃣ GPS Verification

The system requests the student's location through the browser's **Geolocation API**.

The student's coordinates are compared with the attendance location configured by the administrator.

```text
Student GPS
     ↓
Calculate Distance
     ↓
Allowed Radius?
   ↙       ↘
 YES        NO
 ↓          ↓
Continue   Reject
```

This helps prevent attendance from being marked outside the permitted location.

---

## 4️⃣ Face Recognition

After successful location verification, the student's camera is used to capture their face.

The captured face is compared with the student's registered face image.

```text
Registered Face
       +
Captured Face
       ↓
Face Comparison
       ↓
Match?
 ↙         ↘
YES        NO
 ↓          ↓
Allow     Reject
```

---

## 5️⃣ Attendance Storage

After all required verification steps are successful, attendance is stored in the database along with:

* Student
* Date
* Time
* Latitude
* Longitude
* Captured image
* Attendance status

---

# 🗄️ Database Models

### Student

```text
Student
├── name
├── email
├── password
├── roll
└── face_image
```

### Attendance

```text
Attendance
├── student
├── date
├── time
├── latitude
├── longitude
├── image
└── status
```

### Attendance Location

```text
AttendanceLocation
├── name
├── latitude
├── longitude
├── radius
├── is_active
└── created_at
```

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/attendance-system.git
```

```bash
cd attendance-system
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Apply Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## 5. Create Admin Account

```bash
python manage.py createsuperuser
```

Follow the instructions shown in the terminal.

---

## 6. Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Security & Validation

The system uses multiple verification layers:

```text
       LOGIN
         ↓
        OTP
         ↓
        GPS
         ↓
   FACE RECOGNITION
         ↓
    ATTENDANCE
```

This multi-level verification helps reduce:

* Proxy attendance
* Unauthorized attendance
* Attendance from outside the permitted location
* Fake student access

---

# 📱 Mobile Support

The system is designed with a **mobile-first approach**.

Students can use:

* Android smartphones
* iPhones
* Mobile browsers

No dedicated attendance hardware is required.

---

# 🎯 Project Objectives

The main objectives of this project are:

* Automate the attendance process
* Reduce manual attendance work
* Reduce proxy attendance
* Verify student identity
* Verify physical location
* Maintain digital attendance records
* Provide an easy-to-use admin dashboard
* Enable attendance using only a smartphone

---

# 🔮 Future Improvements

Possible future upgrades include:

* 🤖 AI-based face recognition improvements
* 📊 Advanced attendance analytics
* 📈 Attendance percentage dashboard
* 📧 Automated attendance reports
* 📱 Progressive Web App (PWA)
* 🔔 Push notifications
* ☁️ Cloud database integration
* 🔐 Password hashing and improved authentication
* 🧑‍🏫 Teacher-specific dashboards
* 📚 Subject-wise attendance
* 📅 Monthly and semester reports
* 📄 Export attendance to Excel/PDF
* 🛡️ Anti-spoofing / liveness detection

---

# 📊 Example Use Case

### College Classroom

A student enters the classroom and opens the attendance website.

```text
Open Website
     ↓
Login
     ↓
OTP Verification
     ↓
GPS Check
     ↓
Face Verification
     ↓
Attendance Marked
     ↓
Success ✅
```

The teacher/admin can then view the attendance from the dashboard.

---

# 🧪 Testing

The system can be tested using different scenarios:

| Test Case                 | Expected Result         |
| ------------------------- | ----------------------- |
| Valid login               | Login successful        |
| Invalid login             | Access denied           |
| Valid OTP                 | Continue                |
| Expired OTP               | Verification failed     |
| Inside attendance radius  | Location accepted       |
| Outside attendance radius | Location rejected       |
| Matching face             | Verification successful |
| Non-matching face         | Verification failed     |
| Duplicate attendance      | Attendance prevented    |
| Admin login               | Dashboard accessible    |

---

# 👨‍💻 Developer

**Aman**

🎓 Computer Science & Engineering Student

💻 Interested in:

* Python
* Django
* Artificial Intelligence
* Machine Learning
* Data Structures & Algorithms
* Web Development

---

# ⭐ Project Highlights

> **A secure, location-aware and face-verified attendance system that works directly from a student's smartphone.**

### Built with ❤️ using Python & Django

If you find this project useful, consider giving the repository a ⭐.

---

## 📜 License

This project is developed for **educational and academic purposes**.

You are free to study and modify the project for learning purposes.
