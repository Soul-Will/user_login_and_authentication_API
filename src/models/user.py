from database.database import Base
from sqlalchemy import Column,String,ForeignKey,Boolean,DateTime
from datetime import datetime
import uuid

class USER(Base):
    __tablename__ = "user_details"
    id = Column(String(100),nullable=False,primary_key=True)
    username = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False)
    password = Column(String(100),nullable=False)
    country = Column(String(100),nullable=False)
    isActive = Column(Boolean,default=True,nullable=False)
    isVerified = Column(Boolean,default=False,nullable=False)
    isDeleted = Column(Boolean,default=False,nullable=False)
    createdAt = Column(DateTime,default=datetime.now,nullable=False)
    modifiedAt = Column(DateTime,default=datetime.now,onupdate=datetime.now,nullable=False)

class OTP(Base):
    __tablename__ = "otp_details"
    id = Column(String(100),default=str(uuid.uuid4()),primary_key=True,nullable=False)
    user_id = Column(String(100),ForeignKey("user_details.id"),nullable=False)
    email = Column(String(100),nullable=False)
    otp = Column(String(100),nullable=False)
    createdAt = Column(DateTime,default=datetime.now,nullable=False)
    modifiedAt = Column(DateTime,default=datetime.now,onupdate=datetime.now,nullable=False)