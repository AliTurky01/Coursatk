from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey

from database import Base





class users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column("pass", String)
    first_name = Column("fn", String)
    
    # Missing columns added from the schema
    last_name = Column("ln", String)
    department_id = Column("dep_id", Integer, ForeignKey("departments.id"))


class departments(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column("des",String)
    manager_id = Column("m_id", Integer, ForeignKey("users.id"))