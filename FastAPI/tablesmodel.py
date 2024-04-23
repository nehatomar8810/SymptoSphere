from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from .database import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    appointments = relationship("Appointment", back_populates="user")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone_num = Column(String, nullable=True)

class HealthcareProvider(Base):
    __tablename__ = "healthcare_providers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    availability = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone_num = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)

    appointments = relationship("Appointment", back_populates="doctor")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    doctor_email = Column(String, ForeignKey('healthcare_providers.email', ondelete="CASCADE"), nullable=False)
    predicted_diseases = Column(String, nullable=True) #store AI predicted diseases 
    date_time = Column(String, nullable=False)
    status = Column(String, nullable=False) 

    user = relationship("User", back_populates="appointments")
    doctor = relationship("HealthcareProvider", back_populates="appointments")

class PredictedDisease(Base):
    __tablename__ = 'predicted_diseases'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    disease = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

class Precaution(Base):
    __tablename__ = "precautions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diseases = Column(String, nullable=False, unique=True)
    precaution_1 = Column(String, nullable=True)
    precaution_2 = Column(String, nullable=True)
    precaution_3 = Column(String, nullable=True)
    precaution_4 = Column(String, nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    user_id = Column(Integer, primary_key=True)
    doctor_email = Column(String, nullable= False)
    rating = Column(Integer, nullable=False)