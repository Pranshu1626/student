from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

# PyObjectId helper for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Base model with common fields
class BaseModelWithID(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# User models
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: str  # admin, teacher, student, parent
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

# Student models
class StudentBase(BaseModel):
    student_id: str = Field(..., unique=True)
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    current_class: Optional[PyObjectId] = None
    parent_contact: Optional[str] = None
    emergency_contact: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentInDB(StudentBase, BaseModelWithID):
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StudentResponse(StudentBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

# Teacher models
class TeacherBase(BaseModel):
    teacher_id: str = Field(..., unique=True)
    employee_id: Optional[str] = None
    department: Optional[str] = None
    hire_date: Optional[datetime] = None
    specialization: List[str] = []

class TeacherCreate(TeacherBase):
    pass

class TeacherInDB(TeacherBase, BaseModelWithID):
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TeacherResponse(TeacherBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

# Course models
class CourseBase(BaseModel):
    course_code: str = Field(..., unique=True)
    course_name: str
    description: Optional[str] = None
    credits: int = 3
    is_active: bool = True

class CourseCreate(CourseBase):
    pass

class CourseInDB(CourseBase, BaseModelWithID):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CourseResponse(CourseBase):
    id: str
    created_at: datetime
    updated_at: datetime

# Subject models
class SubjectBase(BaseModel):
    subject_code: str = Field(..., unique=True)
    subject_name: str
    course_id: PyObjectId
    description: Optional[str] = None
    is_active: bool = True

class SubjectCreate(SubjectBase):
    pass

class SubjectInDB(SubjectBase, BaseModelWithID):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SubjectResponse(SubjectBase):
    id: str
    course_id: str
    created_at: datetime
    updated_at: datetime

# Class models
class ClassBase(BaseModel):
    class_name: str = Field(..., unique=True)
    grade_level: int
    section: str
    teacher_id: Optional[PyObjectId] = None  # Class teacher
    subject_ids: List[PyObjectId] = []
    student_ids: List[PyObjectId] = []
    academic_year: str

class ClassCreate(ClassBase):
    pass

class ClassInDB(ClassBase, BaseModelWithID):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ClassResponse(ClassBase):
    id: str
    teacher_id: Optional[str] = None
    subject_ids: List[str] = []
    student_ids: List[str] = []
    created_at: datetime
    updated_at: datetime

# Lecture models
class LectureBase(BaseModel):
    lecture_id: str = Field(..., unique=True)
    subject_id: PyObjectId
    teacher_id: PyObjectId
    class_id: PyObjectId
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 45
    is_active: bool = True

class LectureCreate(LectureBase):
    pass

class LectureInDB(LectureBase, BaseModelWithID):
    qr_token: Optional[str] = None
    qr_expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LectureResponse(LectureBase):
    id: str
    subject_id: str
    teacher_id: str
    class_id: str
    qr_token: Optional[str] = None
    qr_expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Attendance models
class AttendanceBase(BaseModel):
    lecture_id: PyObjectId
    student_id: PyObjectId
    status: str  # present, absent, late, excused
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    marked_by: PyObjectId
    qr_scanned: bool = False

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceInDB(AttendanceBase, BaseModelWithID):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AttendanceResponse(AttendanceBase):
    id: str
    lecture_id: str
    student_id: str
    marked_by: str
    created_at: datetime
    updated_at: datetime

# Marks models
class MarksBase(BaseModel):
    student_id: PyObjectId
    subject_id: PyObjectId
    exam_type: str  # midterm, final, quiz, etc.
    exam_name: str
    marks_obtained: float
    total_marks: float
    percentage: float = 0.0
    grade: str = ""
    exam_date: datetime

class MarksCreate(MarksBase):
    pass

class MarksInDB(MarksBase, BaseModelWithID):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MarksResponse(MarksBase):
    id: str
    student_id: str
    subject_id: str
    created_at: datetime
    updated_at: datetime

# Report models
class ReportBase(BaseModel):
    report_type: str
    parameters: dict = {}
    file_path: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportInDB(ReportBase, BaseModelWithID):
    generated_by: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReportResponse(ReportBase):
    id: str
    generated_by: str
    created_at: datetime

# Notification models
class NotificationBase(BaseModel):
    title: str
    message: str
    type: str = "info"  # info, warning, success, error
    is_read: bool = False
    related_id: Optional[PyObjectId] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationInDB(NotificationBase, BaseModelWithID):
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

class NotificationResponse(NotificationBase):
    id: str
    user_id: str
    created_at: datetime
