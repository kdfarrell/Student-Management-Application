# School Management Dashboard

## Overview

School Management Dashboard is a full-stack web application that allows solo teachers to manage their classes from a single interface. Teachers can track students, courses, attendance, grades, and schedules, as well as generate PDF reports and view analytics all in one place.

---

## Motivation

The motivation behind this project came from family members who teach and found themselves managing student records, lesson plans, and classroom data entirely on paper or across disconnected spreadsheets. Building this also served as an opportunity to learn and apply modern technologies, including Vue.js, Django REST Framework, and Tailwind CSS.

By consolidating all of that into one clean, easy-to-use application, the goal was to cover the full scope of full-stack web development — backend API design, JWT authentication, frontend state management, data visualization, and PDF generation.

---

## Goals

### Primary Goals

- Manage students, courses, and enrollments
- Record and track attendance per class session
- Enter and calculate weighted grades per subject
- View an analytics dashboard with at-risk student detection
- Generate and email PDF reports

### Secondary Goals

- Build a clean, responsive UI using modern component libraries
- Practice full-stack integration between Django and Vue 3
- Deepen understanding of state management and API design

---

## Scope & Limitations

### In Scope

- Full CRUD for students, courses, subjects, and enrollments
- Class session scheduling with a weekly calendar view
- Bulk attendance submission per session
- Weighted grade averages with audit logging
- Analytics dashboard with charts and at-risk flagging
- PDF report generation and email delivery

### Out of Scope

- Multi-teacher or school-wide accounts
- Student-facing portal or login
- Mobile app
- Automated or scheduled reporting
- Deployment (built purely for learning)

### Ethical / Legal Considerations

This application stores student data including names, contact details, and academic records. It is intended for personal and educational use only. Users are responsible for ensuring their use complies with applicable data privacy regulations.

---

## Target Users

School Management Dashboard is designed for a single teacher who wants to manage their own classes without relying on multiple disconnected tools. The typical user is comfortable with a web interface and wants a straightforward way to track student progress, attendance, and grades in one place.

---

## Technology Stack

| Layer | Technology | Purpose/Role |
|---|---|---|
| Backend | Python, Django | Server logic and data models |
| API | Django REST Framework | REST API endpoints |
| Auth | SimpleJWT | JWT access and refresh token authentication |
| Frontend | Vue 3, Vite | Component-based UI |
| Styling | Tailwind CSS v4, shadcn-vue | Layout and UI components |
| State Management | Pinia | Global frontend state |
| HTTP Client | Axios | API requests and token interceptors |
| Charts | vue-chartjs, Chart.js | Grade distribution and attendance charts |
| PDF Generation | xhtml2pdf | Server-side PDF report rendering |
| Package Manager | uv | Python dependency and environment management |

---

## System Architecture

School Management Dashboard follows a client–server architecture with a clear separation between the Django backend and the Vue 3 frontend.

The backend is built with Django and Django REST Framework. All API logic is organized across 8 dedicated apps: `users`, `students`, `courses`, `scheduling`, `attendance`, `grades`, `reports`, and `audit`. JWT authentication is handled via SimpleJWT, with all protected endpoints requiring a valid access token.

The frontend is a Vue 3 single-page application scaffolded with Vite. Pinia manages global state across features, and Axios handles all API communication with automatic token attachment and refresh logic via interceptors. UI components are built with shadcn-vue and styled with Tailwind CSS v4.

PDF reports are generated server-side using xhtml2pdf from HTML templates and returned as file responses. Email delivery uses Django's SMTP email backend.

---

## Application Workflow

1. Teacher logs in and receives a JWT access token.
2. The dashboard loads with a summary of students, courses, sessions, and at-risk flags.
3. Teacher creates courses and adds weighted subjects to each.
4. Students are created and enrolled into courses.
5. Class sessions are scheduled and displayed in a weekly calendar view.
6. Attendance is recorded per session using a bulk submission sheet.
7. Assessments are created per subject and grades are entered for each student.
8. Weighted averages are calculated automatically per subject and overall.
9. Every grade change is logged automatically in the audit trail.
10. The dashboard charts update to reflect grade distribution and attendance rates.
11. PDF reports can be generated per student or per course and emailed directly.

---

## Key Features

- JWT login/logout with protected routes and automatic token refresh
- Full student CRUD with search, pagination, and a slide-over detail panel
- Course and subject management with configurable subject weights
- Student enrollment and drop management per course
- Weekly calendar view for scheduling class sessions
- Bulk attendance submission per session with per-student status
- Weighted grade calculation across subjects and assessments
- Automatic audit log on every grade create and update
- Analytics dashboard with stat cards, bar chart, doughnut chart, and at-risk table
- PDF report generation for grades and attendance
- Email delivery of reports via SMTP
- Toast notifications, loading skeletons, and empty states throughout

---

## Implementation Details

- **Authentication:** Custom `Teacher` model extending `AbstractUser`. SimpleJWT issues access (60 min) and refresh (7 day) tokens. Custom token serializer includes teacher name and school in the login response.
- **Student & Course Data:** All queries are filtered to the logged-in teacher so data is fully isolated per user.
- **Weighted Grades:** Calculated as `(score / max_score) × subject.weight`, summed and divided by total weight across all subjects in a course.
- **Audit Logging:** A `log_action()` utility records before and after detail on every grade create and update, stored against the teacher's account.
- **PDF Reports:** HTML templates are rendered server-side with xhtml2pdf and returned as file responses. Three report types are available: student grade report, student attendance report, and course-wide grade report.
- **State Management:** Pinia stores are scoped per feature (students, courses, attendance, grades, dashboard, reports). Axios interceptors handle token attachment and silent refresh on 401 responses.
- **Seed Script:** `initialize_database.py` creates a test superuser and populates the database with sample students, courses, sessions, attendance, and grades for development.

---

## Error Handling & Edge Cases

- Unauthenticated requests return 401; the frontend silently refreshes the token and retries.
- All API errors return a consistent `{"error": "message"}` format.
- Form validation errors are displayed inline using shadcn-vue FormMessage.
- Invalid or missing fields are caught at the serializer level before hitting the database.
- Pagination (20 per page) is applied to all list endpoints.

---

## Security & Performance Considerations

- All endpoints are protected by JWT authentication except login and register.
- Queries are scoped to the logged-in teacher — no cross-user data leakage.
- Sensitive credentials (secret key, SMTP) are stored in a `.env` file and never committed.
- PDF files are generated in memory or cleaned up after delivery.
- Temporary files are not persisted beyond the request lifecycle.

---

## User Interface Design

- Clean, responsive layout built with Tailwind CSS v4 and shadcn-vue components.
- Persistent sidebar navigation with active route highlighting and teacher name in the topbar.
- Feature pages:
  - **Dashboard:** Stat cards, grade distribution bar chart, attendance doughnut chart, at-risk student table
  - **Students:** Searchable data table, slide-over detail panel, create/edit dialog, delete confirmation
  - **Courses:** Course cards, subject editor, enrollment management
  - **Schedule:** Weekly calendar with session cards per day column
  - **Attendance:** Session list with recorded/not-recorded status, bulk submission sheet
  - **Grades:** Tabbed grade entry table, weighted average summary with color-coded badges
  - **Reports:** PDF download forms and email dialog per report type
- Toast notifications (Sonner) on all success and error actions.
- Loading skeletons on all data tables while fetching.
- Empty states with call-to-action buttons on all list views.

---

## Testing Strategy

Testing has been performed manually throughout development.

Test cases included:

- Login, token refresh, and redirect behavior
- Student and course CRUD operations
- Enrollment and drop flows
- Bulk attendance submission and reloading existing records
- Grade entry and weighted average accuracy
- Audit log entries on grade changes
- Dashboard stat accuracy against known database state
- All three PDF report downloads
- Email delivery via SMTP

---

## Challenges & Problems Faced

- Implementing dashboard charts with accurate real-time data from the API
- Calculating and validating weighted grade averages correctly across subjects
- Coordinating frontend and backend during feature integration, particularly around serializer shape and Pinia store structure
- Managing shared and derived state across Pinia stores — keeping the UI in sync when data changed across multiple features

---

## Solutions & Key Learnings

- Built a dedicated `/api/dashboard/` summary endpoint to pre-aggregate chart and stat data server-side, reducing frontend complexity.
- Implemented weighted average logic entirely in the backend as a custom `student_report` action, with thorough manual verification against known scores.
- Established a consistent API response shape early on, which reduced integration friction as features were added.
- Scoped Pinia stores per feature and used actions to encapsulate all API calls, making state changes predictable and easier to debug.
- Gained a strong understanding of how Vue 3 reactivity, Pinia, and Axios interceptors work together in a real application.

---

## Future Improvements

- Package the application with Docker for easier setup and portability
- Add support for multiple teachers with isolated data per account
- Introduce automated testing with pytest (backend) and Vitest (frontend)
- Allow customizable at-risk thresholds per teacher
- Add a student-facing view for report access

---

## Project Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) package manager

Install uv if you don't have it:

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### Backend

```bash
cd backend

# Install dependencies
uv sync

# Activate virtual environment
# macOS / Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Run migrations
uv run manage.py migrate

# Seed the database (also creates a test superuser)
uv run initialize_database.py

# Start the development server
uv run manage.py runserver
```

The backend will be available at `http://127.0.0.1:8000`.

> **Test credentials (created by the seed script):**
> Username: `testteacher` | Password: `testpass`

---

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## Environment Variables

Create a `.env` file inside `backend/` with the following:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Email (SMTP) — used for sending PDF reports
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword
EMAIL_USE_TLS=True
```

> **Never commit `.env` to version control.** It is already included in `.gitignore`.

---

## API Overview

| Endpoint | Description |
|---|---|
| `/api/auth/` | Register, login, token refresh, profile |
| `/api/students/` | Student CRUD |
| `/api/courses/` | Course and subject management |
| `/api/enrollments/` | Student enrollment |
| `/api/sessions/` | Class sessions |
| `/api/attendance/` | Attendance records and bulk submit |
| `/api/assessments/` | Assessments per subject |
| `/api/grades/` | Grade entry and weighted averages |
| `/api/dashboard/` | Summary stats and at-risk data |
| `/api/reports/` | PDF report generation and email |
| `/api/audit/` | Audit log (read-only) |

All endpoints require a valid JWT access token except `/api/auth/login/` and `/api/auth/register/`.

---

## Ethical & Legal Disclaimer

This application stores personal student data including names, contact details, and academic records. It is intended for **personal and educational use only**.

- Users are responsible for ensuring their use complies with applicable data privacy laws.
- The developers are **not responsible** for any misuse of the application.

---

## Conclusion & Reflection

This project provided substantial growth across the full stack:

- Deepened understanding of Django REST Framework, JWT authentication, and API design patterns.
- Gained practical experience with Vue 3, Pinia, and managing complex frontend state across multiple features.
- Learned how to integrate vue-chartjs with real API data and handle edge cases in data visualization.
- Developed confidence in building end-to-end features independently, from database model to UI component.

Overall, the School Management Dashboard represents a complete, feature-rich application built from scratch as a learning project — and a strong foundation for future full-stack development work.