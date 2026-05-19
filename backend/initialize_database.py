import os
import django
import random
from datetime import date, timedelta, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.students.models import Student
from apps.courses.models import Course, Enrollment, Subject
from apps.scheduling.models import ClassSession
from apps.attendance.models import Attendance
from apps.grades.models import Assessment, Grade

# Audit Logging
try:
    from apps.audit.utils import log_audit

    AUDIT_ENABLED = True
except ImportError:
    AUDIT_ENABLED = False

    def log_audit(*args, **kwargs):
        pass


User = get_user_model()


def create_test_teacher():
    username = "testteacher"
    password = "testpass"
    email = "testteacher@test.com"

    if User.objects.filter(username=username).exists():
        print(f"Teacher '{username}' already exists.")
        return User.objects.get(username=username)

    print(f"Creating superuser: {username}")
    teacher = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )

    if hasattr(teacher, "school_name"):
        teacher.school_name = "Academy 101"
        teacher.save()

    print(f"Superuser '{username}' created successfully.")
    return teacher


def populate_development_environment():
    print("Starting Development Environment Population\n")

    teacher = create_test_teacher()

    # Clear existing data
    print("Clearing existing data...")
    Grade.objects.all().delete()
    Assessment.objects.all().delete()
    Attendance.objects.all().delete()
    ClassSession.objects.all().delete()
    Enrollment.objects.all().delete()
    Subject.objects.all().delete()
    Course.objects.all().delete()
    Student.objects.all().delete()

    if AUDIT_ENABLED:
        log_audit(teacher, "CLEAR_DATA", "System", 0, "Cleared all data before reseeding")  # Use 0 instead of None

    # Students
    print("Creating students...")
    student_data = [
        ("Kari", "Van-Dyke", "868-441-1001", "2003-04-12"),
        ("Malik", "Barker", "868-441-1002", "2002-11-30"),
        ("Chloe", "Hammond", "868-441-1003", "2004-01-08"),
        ("Jordan", "Rivers", "868-441-1004", "2003-07-21"),
        ("Aaliyah", "Cross", "868-441-1005", "2002-09-15"),
        ("Devon", "Knight", "868-441-1006", "2003-03-03"),
        ("Elena", "Rostova", "868-441-1007", "2004-06-17"),
        ("Marcus", "Vance", "868-441-1008", "2002-12-25"),
        ("Zara", "Patel", "868-441-1009", "2003-08-09"),
        ("Liam", "Okafor", "868-441-1010", "2003-05-28"),
    ]

    students = []
    for first, last, phone, dob in student_data:
        student = Student.objects.create(
            first_name=first,
            last_name=last,
            email=f"{first.lower()}.{last.lower().replace('-', '')}@example.com",
            phone_number=phone,
            date_of_birth=date.fromisoformat(dob),
            teacher=teacher,
            is_active=True,
        )
        students.append(student)
        if AUDIT_ENABLED:
            log_audit(teacher, "CREATE", "Student", student.id, f"Created student: {first} {last}")

    print(f"Created {len(students)} students.")

    # Courses and Subjects
    print("Creating courses and subjects...")

    course_definitions = [
        {
            "name": "Mathematics 101",
            "description": "Core mathematics course covering algebra and calculus.",
            "subjects": [
                {"name": "Algebra", "description": "Linear equations and expressions.", "weight": 0.50},
                {"name": "Calculus Basics", "description": "Introduction to limits and derivatives.", "weight": 0.50},
            ],
        },
        {
            "name": "Intro to Physics",
            "description": "Foundational physics principles and problem solving.",
            "subjects": [
                {"name": "Mechanics", "description": "Motion, forces, and energy.", "weight": 0.60},
                {"name": "Waves & Optics", "description": "Wave behavior and light.", "weight": 0.40},
            ],
        },
        {
            "name": "English Literature",
            "description": "Critical reading and analysis of literary texts.",
            "subjects": [
                {"name": "Poetry Analysis", "description": "Themes and techniques in poetry.", "weight": 0.40},
                {"name": "Prose & Fiction", "description": "Novel study and narrative structure.", "weight": 0.60},
            ],
        },
        {
            "name": "Computer Science",
            "description": "Programming fundamentals and computational thinking.",
            "subjects": [
                {
                    "name": "Python Programming",
                    "description": "Core Python syntax and problem solving.",
                    "weight": 0.70,
                },
                {"name": "Data Structures", "description": "Arrays, lists, stacks, and queues.", "weight": 0.30},
            ],
        },
    ]

    all_subjects = []

    for course_def in course_definitions:
        course = Course.objects.create(
            name=course_def["name"],
            description=course_def["description"],
            is_active=True,
            teacher=teacher,
        )
        if AUDIT_ENABLED:
            log_audit(teacher, "CREATE", "Course", course.id, f"Created course: {course.name}")

        for student in students:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
                date_enrolled=date(2024, 9, 1),
                status="active",
            )
            if AUDIT_ENABLED:
                log_audit(
                    teacher, "ENROLL", "Enrollment", enrollment.id, f"Enrolled {student.first_name} in {course.name}"
                )

        for subj_def in course_def["subjects"]:
            subject = Subject.objects.create(
                course=course,
                name=subj_def["name"],
                description=subj_def["description"],
                weight=subj_def["weight"],
            )
            all_subjects.append(subject)
            if AUDIT_ENABLED:
                log_audit(teacher, "CREATE", "Subject", subject.id, f"Created subject: {subject.name}")

    # Class Sessions
    print("Creating class sessions (2 per day)...")
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    session_dates = [
        week_start + timedelta(days=week_offset * 7 + day_offset) for week_offset in range(2) for day_offset in range(7)
    ]

    session_slots = [(9, 0, 10, 0), (13, 0, 14, 0)]
    session_count = 0

    for day_idx, session_date in enumerate(session_dates):
        for slot_idx, (start_h, start_m, end_h, end_m) in enumerate(session_slots):
            subject = all_subjects[(day_idx * 2 + slot_idx) % len(all_subjects)]
            room_num = 101 + (all_subjects.index(subject) % 4)

            session = ClassSession.objects.create(
                subject=subject,
                date=session_date,
                start_time=time(hour=start_h, minute=start_m),
                end_time=time(hour=end_h, minute=end_m),
                room=f"Room {room_num}",
                notes=f"{subject.name} - {['Morning', 'Afternoon'][slot_idx]}",
            )
            session_count += 1

            if AUDIT_ENABLED:
                log_audit(
                    teacher,
                    "CREATE",
                    "ClassSession",
                    session.id,
                    f"Created session for {subject.name} on {session_date}",
                )

            for student in students:
                status = random.choices(["present", "late", "absent", "excused"], weights=[70, 15, 10, 5])[0]
                Attendance.objects.create(student=student, session=session, status=status)

    print(f"Created {session_count} class sessions.")

    # Assessments and Grades
    print("Creating assessments and grades...")
    assessment_definitions = [
        {"name": "Quiz 1", "assessment_type": "quiz", "max_score": 25, "date_offset": 0},
        {"name": "Assignment 1", "assessment_type": "assignment", "max_score": 50, "date_offset": 2},
        {"name": "Midterm Exam", "assessment_type": "exam", "max_score": 100, "date_offset": 5},
        {"name": "Test 1", "assessment_type": "test", "max_score": 75, "date_offset": 8},
        {"name": "Final Exam", "assessment_type": "exam", "max_score": 100, "date_offset": 12},
    ]

    for subject in all_subjects:
        for a_def in assessment_definitions:
            assess_date = session_dates[min(a_def["date_offset"], len(session_dates) - 1)]
            assessment = Assessment.objects.create(
                subject=subject,
                name=a_def["name"],
                assessment_type=a_def["assessment_type"],
                max_score=a_def["max_score"],
                date=assess_date,
            )
            if AUDIT_ENABLED:
                log_audit(teacher, "CREATE", "Assessment", assessment.id, f"Created {a_def['name']} for {subject.name}")

            for student in students:
                if random.random() < 0.10:
                    score = round(random.uniform(0, 0.49 * a_def["max_score"]), 1)
                else:
                    score = round(random.uniform(0.55 * a_def["max_score"], a_def["max_score"]), 1)

                grade = Grade.objects.create(
                    student=student,
                    assessment=assessment,
                    score=score,
                    feedback=random.choice(
                        [
                            "Good work",
                            "Needs improvement",
                            "Excellent effort",
                            "Keep it up",
                            "See me after class",
                            "Well done",
                        ]
                    ),
                )
                if AUDIT_ENABLED:
                    log_audit(
                        teacher, "CREATE", "Grade", grade.id, f"Grade for {student.first_name} in {assessment.name}"
                    )

    print("\nDatabase population completed successfully.")
    print(f"Students    : {len(students)}")
    print(f"Courses     : {Course.objects.count()}")
    print(f"Subjects    : {len(all_subjects)}")
    print(f"Sessions    : {ClassSession.objects.count()}")
    print(f"Grades      : {Grade.objects.count()}")


if __name__ == "__main__":
    populate_development_environment()
