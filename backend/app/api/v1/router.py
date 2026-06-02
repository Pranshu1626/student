from fastapi import APIRouter
from app.api.endpoints import auth, users, students, teachers, courses, subjects, classes, lectures, attendance, marks, reports, notifications

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tag=["students"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(lectures.router, prefix="/lectures", tags=["lectures"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(marks.router, prefix="/marks", tags=["marks"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
