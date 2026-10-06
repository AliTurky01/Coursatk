from typing import Literal

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column("des", Text)
    manager_id = Column("m_id", Integer, ForeignKey("users.id", ondelete="SET NULL"))

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column("pass", String(255), nullable=False)
    first_name = Column("fn", String(100), nullable=False)
    last_name = Column("ln", String(100), nullable=False)
    department_id = Column("dep_id", Integer, ForeignKey("departments.id", ondelete="SET NULL"))

class UserCreate(BaseModel):
    email: str
    hashed_password: str
    first_name: str
    last_name: str
    department_id: int | None = None
    role :Literal["student", "employee","admin"]


class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id = Column("uid", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(50), primary_key=True)

class Employee(Base):
    __tablename__ = "emp"
    
    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    hire_date = Column(Date, nullable=False)
    specialization = Column(String(255))

class Student(Base):
    __tablename__ = "student"
    
    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    specialization = Column(String(255))
    degree_level = Column(String(50))

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    hours = Column(Integer, nullable=False)
    description = Column("des", Text)
    department_id = Column("dep_id", Integer, ForeignKey("departments.id", ondelete="CASCADE"))

class Instruction(Base):
    __tablename__ = "instruction"
    
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    employee_id = Column("emp_id", Integer, ForeignKey("emp.id", ondelete="CASCADE"), primary_key=True)

class Enroll(Base):
    __tablename__ = "enroll"
    
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), primary_key=True)